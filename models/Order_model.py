from utilities.database import Base
from sqlalchemy import Column,String,Integer,DateTime,Text,ForeignKey,Numeric
from datetime import datetime
class Order(Base):
    __tablename__="orders_1"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users_7.id"))
    order_date=Column(DateTime,default=datetime.utcnow)
    total_amount=Column(Numeric)
    payment_status=Column(String,default="pending")
    order_status=Column(String)
    shipping_address=Column(Text)
    billing_address=Column(Text)
    delivery_date=Column(DateTime,default=datetime.utcnow)
    cancelled_at=Column(DateTime,default=datetime.utcnow)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)