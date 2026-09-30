from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
class OrderitemRequest(BaseModel):
    order_id:int
    product_id:int
    quantity:int
    price:Decimal
    created_at:datetime
    updated_at:datetime