from pydantic import BaseModel,EmailStr
class ResetOTPRequest(BaseModel):
    email:EmailStr