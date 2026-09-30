from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
class CartRequest(BaseModel):
    product_id:int
    quantity:int
    price:Decimal
    subtotal:Decimal
    added_at:datetime
    created_at:datetime
    updated_at:datetime