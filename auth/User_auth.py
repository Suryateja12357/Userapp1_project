from fastapi import APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from utilities.database import SessionLocal
from sqlalchemy.orm import Session
from models.User_model import User
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
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

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

# @router.post("/login")
# async def login(db:db_dependency,email:str,password:str):
#     try:
#         user_model=db.query(User).filter(User.email==email).first()
#         if not user_model:
#             raise HTTPException(status_code=404,detail="User is not found")
#         if not verify_password(password,user_model.password):
#             raise HTTPException(status_code=401,detail="invalid password")
#         if not user_model.is_verified:
#             raise HTTPException(status_code=403,detail="please verify your email first")
#         token=create_access_token(data={"sub":str(user_model.id)})
#         return{"message":"Login successful","user_id":user_model.id,"email":user_model.email,"access_token":token,"token_type":"bearer"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"something went wrong:{str(e)}")