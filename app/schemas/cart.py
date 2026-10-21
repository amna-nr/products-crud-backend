from pydantic import BaseModel


class CartProductUpdate(BaseModel):
    id: int
    quantity: int

