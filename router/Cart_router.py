from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from auth.User_auth import get_current_user
from auth.User_auth import create_access_token
from models.Cart_model import Cart
from models.User_model import User
from Validation.Cart_validation import CartRequest

router=APIRouter()

def gt_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(gt_db)]
user_dependency=Annotated[User,Depends(get_current_user)]

@router.get("/cart/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,user:user_dependency):
    return db.query(Cart).all()

@router.get("/cart/{cart_id}",status_code=status.HTTP_200_OK)
async def read_cart(db:db_dependency,user:user_dependency,cart_id:int=Path(gt=0)):
    try:
        cart_model=db.query(Cart).filter(Cart.id==cart_id).first()
        if cart_model is None:
            raise HTTPException(status_code=404,detail="cart is not found")
        token=create_access_token(data={"sub":cart_model.user_id})
        return {"access_token":token,"token_type":"bearer","cart_model":cart_model.user_id}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.post("/cart/",status_code=status.HTTP_201_CREATED)
async def create_cart(db:db_dependency,cart_request:CartRequest,user:user_dependency):
    try:
        cart_model=Cart(user_id=user.id,
                        product_id=cart_request.product_id,
                        quantity=cart_request.quantity,
                        price=cart_request.price)
        db.add(cart_model)
        db.commit()
        token=create_access_token(data={"sub":cart_model.product_id})
        return{"access_token":token,"token_type":"bearer","cart_model":cart_model}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.put("/cart/{cart_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_cart(db:db_dependency,cart_id:int,cart_request:CartRequest,user:user_dependency):
    try:
        cart_model=db.query(Cart).filter(Cart.id==cart_id).first()
        if cart_model is None:
            raise HTTPException(status_code=404,detail="cart is not found")
        cart_model.user_id=cart_request.user_id
        cart_model.product_id=cart_request.product_id
        cart_model.quantity=cart_request.quantity
        cart_model.price=cart_request.price
        cart_model.subtotal=cart_request.subtotal
        cart_model.added_at=cart_request.added_at
        cart_model.created_at=cart_request.created_at
        cart_model.updated_at=cart_request.updated_at
        db.add(cart_model)
        db.commit()
        token=create_access_token(data={"sub":cart_model.id})
        return{"access_token":token,"access_type":"bearer",cart_model:"cart_model"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/cart/{cart_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(db:db_dependency,cart_id:int,user:user_dependency):
    try:
        cart_model=db.query(Cart).filter(cart_id==Cart.id).first()
        if cart_model is None:
            raise HTTPException(status_code=404,detail="cart is not found")
        db.query(Cart).filter(Cart.id==cart_id).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))