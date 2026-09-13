from pydantic import BaseModel
class UserDeactivateRequest(BaseModel):
    email:str
    password:str
    