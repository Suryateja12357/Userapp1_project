from utilities.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from datetime import datetime
class Wishlist(Base):
    __tablename__="wishlist"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users_7.id"))
    product_id=Column(Integer,ForeignKey("products_1.id"))
    added_at=Column(DateTime,default=datetime.utcnow)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)