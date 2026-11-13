from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str
    user_phone_number: int
    user_description: str

class ProfileUpdate(BaseModel):
    user_name: str
    user_description: str