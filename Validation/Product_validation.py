from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
class ProductRequest(BaseModel):
    name:str
    description:str
    price:Decimal
    stock_quantity:int
    brand:str
    image_url:str
    status:str
    created_at:datetime
    updated_at:datetime