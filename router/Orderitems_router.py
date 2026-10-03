from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from models.Orderitems_model import Orderitems
from Validation.Orderitems_validation import OrderitemRequest
from models.User_model import User
from models.Order_model import Order
from models.Product_model import Product
from auth.User_auth import get_current_user
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[User,Depends(get_current_user)]

@router.get("/orderitems",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,user:user_dependency):
    return(db.query(Orderitems).join(Order,Orderitems.order_id==Order.id).filter(Order.user_id==user.id).all())

@router.get("/orderitems/{orderitem_id}",status_code=status.HTTP_200_OK)
async def read_orderitems(db:db_dependency,user:user_dependency,orderitem_id:int=Path(gt=0)):
    try:
        orderitem_model=db.query(Orderitems).join(Order,Orderitems.id==Order.id).filter(Orderitems. id==orderitem_id,Order.user_id==user.id).first()
        if orderitem_model is None:
            raise HTTPException(status_code=404,detail="orderitem is not found")
        return orderitem_model
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        

@router.post("/orderitems",status_code=status.HTTP_201_CREATED)
async def create_orderitems(db:db_dependency,orderitem_request:OrderitemRequest,user:user_dependency):
    try:
        order_model=db.query(Order).filter(Order.id==orderitem_request.order_id,
                                           Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="Order not found")
        product_model=db.query(Product).filter(Product.id==orderitem_request.product_id).first()
        if product_model is None:
            raise HTTPException(status_code=404,detail="Product not found")
        if order_model.order_status=="cancelled":
            raise HTTPException(status_code=400,detail="Cannot add items to a cancelled order")
        orderitem_model=Orderitems(order_id=order_model.id,
                                   product_id=product_model.id,
                                   quantity=orderitem_request.quantity,
                                   price=product_model.price)
        db.add(orderitem_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.put("/orderitems/{orderitem_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_orderitems(db:db_dependency,orderitem_id:int,orderitem_request:OrderitemRequest,user:user_dependency):
    try:
        orderitem_model=db.query(Orderitems).join(Order,Orderitems.id==Order.id).filter(Orderitems.id==orderitem_id,Order.user_id==user.id).first()
        if orderitem_model is None:
            raise HTTPException(status_code=404,detail="orderitem is not found")
        orderitem_model.order_id=orderitem_request.order_id
        orderitem_model.product_id=orderitem_request.product_id
        orderitem_model.quantity=orderitem_request.quantity
        orderitem_model.price=orderitem_request.price
        orderitem_model.created_at=orderitem_request.created_at
        orderitem_model.updated_at=orderitem_request.updated_at
        db.add(orderitem_model)
        db.commit()
        return {"orderitem":orderitem_model}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/orderitems/{orderitem_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_orderitems(db:db_dependency,orderitem_id:int,user:user_dependency):
    try:
        orderitem_model=db.query(Orderitems).filter(Orderitems.id==orderitem_id).first()
        if orderitem_model is None:
            raise HTTPException(status_code=404,detail="orderitem is not found")
        order_model=db.query(Order).filter(Order.id==orderitem_model.order_id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order is not found")
        if order_model.user_id!=user.id:
            raise HTTPException(status_code=403,detail="You are not authorized to delete this order item")
        db.query(Orderitems).filter(orderitem_id==Orderitems.id).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))