from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal  
class OrderRequest(BaseModel):
    order_date:datetime
    total_amount:Decimal
    payment_status:str
    order_status:str
    shipping_address:str
    billing_address:str
    delivery_date:datetime
    cancelled_at:datetime
    created_at:datetime
    updated_at:datetime