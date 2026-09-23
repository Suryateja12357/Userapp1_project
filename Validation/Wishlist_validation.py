from pydantic import BaseModel
from datetime import datetime
class WishlistRequest(BaseModel):
    user_id:int
    product_id:int
    added_at:datetime
    created_at:datetime
    updated_at:datetime