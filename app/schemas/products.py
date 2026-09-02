from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int
    quantity: int

class ProductUpdate(BaseModel):
    name: str 
    price: int 
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    quantity: int
    