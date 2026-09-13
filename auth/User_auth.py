from fastapi import APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from auth.User_verification import send_verification_email
from auth.User_otp import send_otp_email
from auth.User_deactivation import send_deactivate_email
from auth.Userotp import send_resend_otp
from utilities.database import SessionLocal
from sqlalchemy.orm import Session
from models.User_model import User
from Validation.User_validation import UserValidation
from Validation.Resetpassword_validation import ResetPasswordRequest
from Validation.Forgotpassword_validation import ForgotPasswordRequest
from Validation.Userdeactivation_validation import UserDeactivateRequest
from auth.User_otp import generate_otp
from auth.User_otp import generate_otp
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
router=APIRouter()

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/user/login"
)
token_dependency=Annotated[str,Depends(oauth2_scheme)]

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

bcrypt_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hash_password:str):
    return pwd_context.verify(plain_password,hash_password)

SECRET_KEY="wYx47urFsAenoumb6wSHTvLnqd4_U6h0Q4fnVwS6syY"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    

def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")

async def get_current_user(token:token_dependency,db:db_dependency):
    user_id=verify_token(token)
    user_model=db.query(User).filter(User.id==int(user_id)).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail="user is not found")
    return user_model

async def admin_authorization(current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="You are not authorized")
    return current_user

@router.post("/signup")
def signup(user_validation:UserValidation,db:db_dependency):
    existing_user=db.query(User).filter(User.email==user_validation.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed_password=pwd_context.hash(user_validation.password)
    new_user=User(
        user_name=user_validation.name,
        email=user_validation.email,
        password=hashed_password,
        full_name=user_validation.full_name,
        phone_number=user_validation.phone_number,
    )
    db.add(new_user)
    db.commit()
    token=create_access_token(data={"sub":new_user.email})
    send_verification_email(new_user.email,token)

@router.post("/resetpassword")
def resetpassword(request:ResetPasswordRequest,db:db_dependency):
    user=db.query(User).filter(User.email==request.email).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    user.password=bcrypt_context.hash(request.new_password)
    otp=generate_otp()
    user.reset_otp=otp
    send_otp_email(user.email,otp)
    return {"message":"Reset OTP send to your mail"}

@router.post("/forgotpassword")
def forgot_password(db:db_dependency,request:ForgotPasswordRequest):
    user=db.query(User).filter(User.email==request.email).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user is not registered")
    otp=generate_otp()
    user.reset_otp=otp
    # token=create_access_token(data={"sub":user.email,"type":"password_reset"})
    send_otp_email(user.email,otp)
    return {"message":"Password reset verification email sent"}

@router.post("/deactivate")
def deactivate_user(request:UserDeactivateRequest,db:db_dependency):
    user=db.query(User).filter(User.email==request.email).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user is not found")
    if not bcrypt_context.verify(request.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid password")
    user.is_active=False
    db.commit()
    send_deactivate_email(user.email)
    return {"message":"User deactivated successfully"}

@router.get("/verifyemail")
def verify_email(token:str,db:db_dependency,email:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400,detail="Invalid or expired token")
    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=404,detail="user is not found")
    user.is_verified=True
    db.commit()
    return {"message":"Email verified successfully"}