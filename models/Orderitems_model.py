from utilities.database import Base
from sqlalchemy import Column,Integer,Numeric,DateTime,ForeignKey
from datetime import datetime
class Orderitems(Base):
    __tablename__="orderitems"
    id=Column(Integer,index=True,primary_key=True)
    order_id=Column(Integer,ForeignKey("orders_1.id"))
    product_id=Column(Integer,ForeignKey("products_1.id"))
    quantity=Column(Integer)
    price=Column(Numeric(10,2))
    created_at=Column(DateTime,default=datetime)
    updated_at=Column(DateTime,default=datetime,onupdate=datetime.utcnow)