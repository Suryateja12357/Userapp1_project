from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from models.Order_model import Order
from Validation.Order_validation import OrderRequest
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/order/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Order).all()

@router.get("/order/{order_id}",status_code=status.HTTP_200_OK)
async def read_order(db:db_dependency,order_id:int=Path(gt=0)):
    order_model=db.query(Order).filter(Order.id==order_id).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=404,detail="order is not found")

@router.post("/order/",status_code=status.HTTP_201_CREATED)
async def create_order(db:db_dependency,order_request:OrderRequest):
    order_model=Order(**order_request.dict())
    db.add(order_model)
    db.commit()
    return order_model

@router.put("/order/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_order(db:db_dependency,order_id:int,order_request:OrderRequest):
    order_model=db.query(Order).filter(Order.id==order_id).first()
    if order_model is None:
        raise HTTPException(status_code=404,detail="order is not found")
    order_model.user_id=order_request.user_id
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
    return order_model

@router.delete("/order/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(db:db_dependency,order_id:int):
    order_model=db.query(Order).filter(order_id==Order.id).first()
    if order_model is None:
        raise HTTPException(status_code=404,detail="order is not found")
    db.query(Order).filter(Order.id==order_id).delete()
    db.commit()