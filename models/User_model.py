from utilities.database import Base
from sqlalchemy import Column,String,Integer,Boolean,DateTime
from datetime import datetime
class User(Base):
    __tablename__="users_7"
    id=Column(Integer,primary_key=True,index=True)
    user_name=Column(String)
    email=Column(String)
    password=Column(String)
    full_name=Column(String)
    phone_number=Column(Integer)
    is_active=Column(Boolean,default=True)
    role=Column(String)
    is_verified=Column(Boolean,default=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)