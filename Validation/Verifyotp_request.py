from pydantic import BaseModel,Field
class VerifyOTPRequest(BaseModel):
    email:str
    otp:str=Field(max_length=6)