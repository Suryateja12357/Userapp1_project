from fastapi import APIRouter,Depends,BackgroundTasks
from fastapi import HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
import secrets
from models.User_model import User
from Validation.Verifyotp_request import VerifyOTPRequest
from passlib.context import CryptContext
from datetime import datetime,timezone,timedelta
from auth.User_auth import get_current_user,admin_authorization
from auth.User_auth import create_access_token
from auth.User_OTP1 import send_otp_email
from auth.User_resetotp import send_reset_otp
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/login")

router=APIRouter(
    prefix="/user",
    tags=["User"]
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
current_user=Annotated[User,Depends(get_current_user)]
admin_user=Annotated[User,Depends(admin_authorization)]

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)
def generate_otp():
    otp=f"{secrets.randbelow(1000000):6d}"
    return otp

@router.get("/")
async def read_all(db:db_dependency):
    return db.query(User).all()

@router.post("/sign_up")
async def signup(db:db_dependency,email:str,user_name:str,password:str,background_tasks:BackgroundTasks):
    try:
        existing_email=db.query(User).filter(User.email==email).first()
        if existing_email and existing_email.is_verified:
            raise HTTPException(status_code=400,detail="Email already registered")
        otp=generate_otp()
        if existing_email:
            user_model=existing_email
            user_model.user_name=user_name
            user_model.password=pwd_context.hash(password)
        else:
            user_model=User(email=email,user_name=user_name,password=pwd_context.hash(password))
            db.add(user_model)
        user_model.otp=otp
        user_model.email_verification_expiry=(
            datetime.now(timezone.utc)+timedelta(minutes=5)
        )
        db.commit()
        background_tasks.add_task(send_otp_email,email,otp)
        return{"message":"OTP sent to your email.Please verify in 5 minutes."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Something went wrong:{str(e)}")

@router.post("/verify_otp")
async def verify_otp(request:VerifyOTPRequest,db:db_dependency):
    try:
        user_model=db.query(User).filter(User.email==request.email,User.email_verification_otp==request.otp).first()
        if user_model is None:
            raise HTTPException(status_code=404,detail="user is not found")
        if user_model.is_verified:
            return{"message":"Email already verified"}
        if user_model.email_verification_otp is None:
            raise HTTPException(status_code=400,detail="Please request new OTP")
        if str(user_model.email_verification_otp)!=str(request.otp):
            raise HTTPException(status_code=400,detail="Invalid OTP")
        expiry=user_model.email_verification_expiry
        if expiry is None:
            raise HTTPException(status_code=400,detail="OTP expiry is missing.Please request new OTP")

        if expiry.tzinfo is None:
            expiry=expiry.replace(tzinfo=timezone.utc)
        if expiry<=datetime.now(timezone.utc):
            raise HTTPException(status_code=400,detail="OTP expired. please request a new OTP")
        user_model.is_verified=True
        user_model.email_verification_otp=None
        user_model.email_verification_expiry=None
        db.commit()
        return{"message":"Email and OTP verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))



@router.get("/forgot_password")
async def forgot_password(db:db_dependency,email:str):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="user is not found")
        token=create_access_token(data={"sub":user_model.email})
        return {"message":"Password reset link will be sent to your email","access_token":token,"token_type":"bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error:{e}")
        raise HTTPException(status_code=500,detail="Something went wrong")

@router.put("/reset_password")
async def reset_password(db:db_dependency,email:str,new_password:str,old_password:str):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="user is not found")
        if not verify_password(old_password,user_model.password):
            raise HTTPException(status_code=400,detail="Old password is incorrect")
        user_model.password=hash_password(new_password)
        db.commit()
        return {"message":"Password reset successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Something went wrong:{(e)}")



@router.post("/user_deactivate")
async def user_deactivate(db:db_dependency,user_id:int):
    try:
        user_model=db.query(User).filter(User.id==user_id).first()
        if user_model is None:
            raise HTTPException(status_code=404,detail='user is not found')
        user_model.is_active=False
        db.commit()
        # token=create_access_token(data={"sub":user_model.full_name})
        return {'message':'User deactivated successfully','user_id':user_model.id,'user':user_model.full_name,'is_active':user_model.is_active}
        #return current_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"something went wrong:{str(e)}")

@router.delete("/{user_id}")
async def delete_user(db:db_dependency,user_id:int):
    user_model=db.query(User).filter(User.id==user_id).first()
    try:
        if user_model is None:
            raise HTTPException(status_code=404,detail="user is not found")
        #token=create_access_token(data={"sub":user_model.full_name})
        db.query(User).filter(User.id==user_id).delete()
        db.commit()
        #return {"message":"deletion successfully","user":user_model.full_name,"access_token":token,"token_type":"bearer"}
        # return current_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"something went to wrong:{str(e)}")

@router.put("/{user_id}/email")
async def update_email(db:db_dependency,user_id:int,email:str):
    try:
        user_model=db.query(User).filter(User.id==user_id).first()
        if user_model is None:
            raise HTTPException(status_code=404,detail="user is not found")
        user_model.email=email
        db.commit()
        token=create_access_token(data={"sub":user_model.email})
        return {"message":"Email updated successfully","user_id":user_model.id,"user_email":user_model.email,"access_token":token,"token_type":"bearer"}
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=505,detail=f"something went wrong:{str(e)}")

@router.put("/{user_id}/phone")
async def update_mobile_number(db:db_dependency,user_id:int,phone_number:int):
    user_model=db.query(User).filter(User.id==user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail="user is not found")
    user_model.phone_number=phone_number
    db.commit()
    token=create_access_token(data={"sub":user_model.phone_number})
    return{"message":"phone number updated successfully","user_id":user_model.id,"user_phone_number":user_model.phone_number,"access_token":token,"token_type":"bearer"}
    # return current_user
@router.post("/login")
async def login(db:db_dependency,form_data:OAuth2PasswordRequestForm=Depends()):
    user=db.query(User).filter((User.email==form_data.username)|(User.user_name==form_data.username)).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    if not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid password")
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="please verify your email first")
    if not user.is_active:
        raise HTTPException(status_code=403,detail="User account is inactive")
    access_token=create_access_token(data={"sub":str(user.id)})
    return {"access_token":access_token,"token_type":"bearer"}


@router.post("/reset_otp")
async def reset_otp(email:str,db:db_dependency,background_tasks:BackgroundTasks):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if user_model is None:
            raise HTTPException(status_code=404,detail="user is not found")
        otp=f"{secrets.randbelow(1000000):06d}"
        user_model.reset_otp=otp
        user_model.reset_otp_expiry=(datetime.now(timezone.utc)+timedelta(minutes=5))
        db.commit()
        background_tasks.add_task(send_reset_otp,user_model.email,otp)
        return{"message":"Reset OTP sent to your email"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Failed to generate reset OTP")