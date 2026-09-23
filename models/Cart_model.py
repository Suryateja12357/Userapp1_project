from  utilities.database import Base
from sqlalchemy import Column,String,Integer,DateTime,Numeric,ForeignKey
#from decimal import Decimal
from datetime import datetime
class Cart(Base):
    __tablename__="cart"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users_7.id"))
    product_id=Column(Integer,ForeignKey("products_1.id"))
    quantity=Column(Integer)
    price=Column(Numeric)
    subtotal=Column(Numeric)
    added_at=Column(DateTime,default=datetime.utcnow)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)