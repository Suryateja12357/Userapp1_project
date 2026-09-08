from fastapi import APIRouter,Depends
from fastapi import HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from models.User_model import User
from passlib.context import CryptContext
from auth.User_auth import get_current_user,admin_authorization
from auth.User_auth import create_access_token

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
current_user=Annotated[User,Depends(get_current_user)]

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

@router.get("/user/")
async def read_all(db:db_dependency):
    return db.query(User).all()

@router.post("/user/login")
async def login(db:db_dependency,email:str,password:str):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="user is not found")
        if not verify_password(password,user_model.password):
            raise HTTPException(status_code=401,detail="invalid password")
        if not user_model.is_verified:
            raise HTTPException(status_code=403,detail="Please verify your email first")
        token=create_access_token(data={"sub":str(user_model.id)})
        return {"message":"login successful","access_token":token,"token_type":"bearer"}
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Something went wrong:{str(e)}")
    

@router.post("/sign_up")
async def signup(db:db_dependency,email:str,password:str):
    try:
        existing_user=db.query(User).filter(User.email==email).first()
        if existing_user:
            raise HTTPException(status_code=400,detail="Email already registered")
        hashed_password=hash_password(password)
        user_model=User(email=email,password=hashed_password)
        db.add(user_model)
        db.commit()
        return{"message":"User registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Something went wrong:{str(e)}")

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
async def reset_password(db:db_dependency,email:str,new_password:str):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="user is not found")
        user_model.password=hash_password(new_password)
        db.commit()
        return {"message":"Password reset successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Something went wrong:{(e)}")

@router.get("/verify_email")
async def verify_email(email:str,db:db_dependency):
    try:
        user_model=db.query(User).filter(User.email==email).first()
        if not user_model:
            raise HTTPException(status_code=404,detail="User not found")
        user_model.is_verified=True
        db.commit()
        return {"message":"Email verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"something went wrong:{str(e)}")

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

@router.delete("/user/{user_id}")
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

@router.put("/user/{user_id}/email")
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

@router.put("/user/{user_id}/phone")
async def update_mobile_number(db:db_dependency,user_id:int,phone_number:int):
    user_model=db.query(User).filter(User.id==user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail="user is not found")
    user_model.phone_number=phone_number
    db.commit()
    token=create_access_token(data={"sub":user_model.phone_number})
    return{"message":"phone number updated successfully","user_id":user_model.id,"user_phone_number":user_model.phone_number,"access_token":token,"token_type":"bearer"}
    # return current_user