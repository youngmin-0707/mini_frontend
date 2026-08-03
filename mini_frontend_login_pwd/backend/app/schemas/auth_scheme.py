# auth_scheme.py
from pydantic import BaseModel, Field

class AuthCreate(BaseModel):
    id:str
    pwd:str
    name:str

class AuthLogin(BaseModel):
    id:str
    pwd:str


class AuthPasswordUpdate(BaseModel):
    id:str
    current_pwd:str = Field(min_length=4)
    new_pwd:str = Field(min_length=4)
    
class AuthPublic(BaseModel):
    id:str
    name:str | None = None