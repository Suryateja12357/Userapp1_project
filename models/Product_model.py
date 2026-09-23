from utilities.database import Base
from sqlalchemy import Column,String,Integer,Boolean,DateTime,Numeric,ForeignKey
from datetime import datetime
class Product(Base):
    __tablename__="products_1"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    price=Column(Numeric(10,2))
    stock_quantity=Column(Integer)
    brand=Column(String)
    image_url=Column(String)
    status=Column(String)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)