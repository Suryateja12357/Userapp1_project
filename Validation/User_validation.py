from pydantic import BaseModel
class UserValidation(BaseModel):
    name:str
    email:str
    password:str
    full_name:str
    phone_number:int