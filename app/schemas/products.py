from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int
    stock_quantity: int

class ProductUpdate(BaseModel):
    name: str
    price: int
    stock_quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock_quantity: int

class ProductAddToCart(BaseModel):
    id: int
    quantity: int