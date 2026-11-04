from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from models.Orderitems_model import OrderItems
from Validation.Orderitems_validation import OrderItemRequest
from models.User_model import User
from models.Order_model import Order
from models.Product_model import Product
from auth.User_auth import get_current_user,admin_authorization
router=APIRouter(
    prefix="/order_items",
    tags=["Order_items"]
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[User,Depends(get_current_user)]
admin_user=Annotated[User,Depends(admin_authorization)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,user:user_dependency):
    try:
        return(db.query(OrderItems).join(Order,OrderItems.order_id==Order.id).filter(Order.user_id==user.id).all())
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")

@router.get("/{order_item_id}",status_code=status.HTTP_200_OK)
async def read_order_items(db:db_dependency,user:user_dependency,order_item_id:int=Path(gt=0)):
    try:
        order_item_model=db.query(OrderItems).join(Order,OrderItems.id==Order.id).filter(OrderItems. id==order_item_id,Order.user_id==user.id).first()
        if order_item_model is None:
            raise HTTPException(status_code=404,detail="order_item is not found")
        return order_item_model
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")
        
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_order_items(db:db_dependency,user:user_dependency,order_item_request:OrderItemRequest):
    try:
        order_model=db.query(Order).filter(Order.id==order_item_request.order_id,
                                           Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="Order not found")
        product_model=db.query(Product).filter(Product.id==order_item_request.product_id).first()
        if product_model is None:
            raise HTTPException(status_code=404,detail="Product not found")                     
        if order_item_request.quantity<=0:
            raise HTTPException(status_code=400,detail="Quantity must be greater than zero")
        order_item_model=OrderItems(order_id=order_model.id,
                                   product_id=product_model.id,
                                   quantity=order_item_request.quantity,
                                   price=product_model.price)
        db.add(order_item_model)
        db.commit()
        return order_item_model
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")

@router.put("/{order_item_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_order_items(db:db_dependency,order_item_id:int,order_item_request:OrderItemRequest,user:user_dependency):
    try:
        order_item_model=db.query(OrderItems).filter(OrderItems.id==order_item_id).first()
        if order_item_model is None:
            raise HTTPException(status_code=404,detail="order_item is not found")
        if order_item_request.quantity<=0:
            raise HTTPException(status_code=400,detail="quantity must be greater than zero")
        product_model=db.query(Product).filter(Product.id==order_item_request.product_id).first()
        order_model=db.query(Order).filter(Order.id==order_item_model.order_id,Order.user_id==user.id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order item is not found")
        if product_model is None:
            raise HTTPException(status_code=404,detail="Product is not found")
        if order_model.order_status!="pending":
            raise HTTPException(status_code=400,detail="only pending orders can be updated")
        order_item_model.product_id=product_model.id
        order_item_model.quantity=order_item_request.quantity
        order_item_model.price=product_model.price
        order_item_model.created_at=order_item_request.created_at
        order_item_model.updated_at=order_item_request.updated_at
        db.add(order_item_model)
        db.commit()
        return {"orderItem":order_item_model}
    except Exception:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")

@router.delete("/{order_item_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_items(db:db_dependency,order_item_id:int,user:user_dependency):
    try:
        order_item_model=db.query(OrderItems).filter(OrderItems.id==order_item_id).first()
        if order_item_model is None:
            raise HTTPException(status_code=404,detail="orderItem is not found")
        order_model=db.query(Order).filter(Order.id==order_item_model.order_id).first()
        if order_model is None:
            raise HTTPException(status_code=404,detail="order item is not found")
        if order_model.order_status!="pending":
            raise HTTPException(status_code=400,detail="Only pending orders can be modified")
        db.query(OrderItems).filter(order_item_id==OrderItems.id).delete()
        db.commit()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail="Internal server error")