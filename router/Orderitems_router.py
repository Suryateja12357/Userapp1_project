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
from auth.User_auth import get_current_user
from auth.User_auth import create_access_token
from auth.User_auth import OAuth2PasswordBearer
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
    return db.query(Orderitems).all()

@router.get("/orderitems/{orderitem_id}",status_code=status.HTTP_200_OK)
async def read_orderitems(db:db_dependency,user:user_dependency,orderitem_id:int=Path(gt=0)):
    try:
        orderitem_model=db.query(Orderitems).filter(Orderitems.id==Order.id).filter(Orderitems.     id==orderitem_id).first()
        if orderitem_model is None:
            raise HTTPException(status_code=404,detail="orderitem is not found")
        token=create_access_token(data={"sub":orderitem_model.id})
        return {"access_token":token,"token_type":"bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        

@router.post("/orderitems",status_code=status.HTTP_201_CREATED)
async def create_orderitems(db:db_dependency,orderitem_request:OrderitemRequest,user:user_dependency):
    try:
        orderitem_model=Orderitems(order_id=orderitem_request.order_id,
                                   product_id=orderitem_request.product_id,
                                   quantity=orderitem_request.quantity,
                                   price=orderitem_request.price)
        db.add(orderitem_model)
        db.commit()
        token=create_access_token(data={"sub":orderitem_model.id})
        return {"access_token":token,"token_type":"bearer","orderitem":orderitem_model}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.put("/orderitems/{orderitem_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_orderitems(db:db_dependency,orderitem_id:int,orderitem_request:OrderitemRequest,user:user_dependency):
    try:
        orderitem_model=db.query(Orderitems).filter(Orderitems.id==orderitem_id).first()
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
        token=create_access_token(data={"sub":orderitem_model.id})
        return {"access_token":token,"token_type":"bearer","orderitem":orderitem_model}
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
        if order_model.user_id!=user["id"]:
            raise HTTPException(status_code=403,detail="You are not authorized to delete this order item")
        db.query(Orderitems).filter(orderitem_id==Orderitems.id).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))