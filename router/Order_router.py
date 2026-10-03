from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from auth.User_auth import get_current_user
from models.Order_model import Order
from models.User_model import User
from Validation.Order_validation import OrderRequest
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[User,Depends(get_current_user)]

@router.get("/order/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,user:user_dependency):
    return db.query(Order).filter(Order.user_id==user.id).all()

@router.get("/order/{order_id}",status_code=status.HTTP_200_OK)
async def read_order(db:db_dependency,user:user_dependency,order_id:int=Path(gt=0)):
    try:
        order_model=db.query(Order).filter(Order.id==order_id,
                                           Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order is not found")
        return{"order_model":order_model}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.post("/order/",status_code=status.HTTP_201_CREATED)
async def create_order(db:db_dependency,order_request:OrderRequest,user:user_dependency):
    try:
        order_model=Order(user_id=user.id,
                          total_amount=order_request.total_amount,
                          payment_status=order_request.payment_status,
                          order_status=order_request.order_status,
                          shipping_address=order_request.shipping_address,
                          billing_address=order_request.billing_address,
                          created_at=order_request.created_at,
                          updated_at=order_request.updated_at)
        db.add(order_model)
        db.commit()
        return {"message":"Order created successfully","order_model":order_model}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.put("/order/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_order(db:db_dependency,order_id:int,order_request:OrderRequest,user:user_dependency):
    try:
        order_model=db.query(Order).filter(Order.id==order_id,
                                           Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order is not found")
        order_model.order_date=order_request.order_date
        order_model.total_amount=order_request.total_amount
        order_model.payment_status=order_request.payment_status
        order_model.order_status=order_request.order_status
        order_model.shipping_address=order_request.shipping_address
        order_model.billing_address=order_request.billing_address
        order_model.delivery_date=order_request.delivery_date
        order_model.cancelled_at=order_request.cancelled_at
        order_model.created_at=order_request.created_at
        order_model.updated_at=order_request.updated_at
        db.add(order_model)
        db.commit()
        return{"order_model":order_model}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/order/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(db:db_dependency,order_id:int,user:user_dependency):
    try:
        order_model=db.query(Order).filter(Order.id==order_id,
                                           Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order is not found")
        db.query(Order).filter(order_id==Order.id).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))