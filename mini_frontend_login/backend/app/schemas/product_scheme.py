# product_scheme.py
from pydantic import BaseModel, Field

class ProductPublic(BaseModel):
    id:int
    name:str
    price:int


class ProductUpdate(BaseModel):
    name:str
    price:int