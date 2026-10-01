from uuid import UUID
from fastapi import APIRouter, Cookie
from app.core.database import db_dependency
from app.services.cart import get_cart_products, add_product_to_cart
from app.schemas.products import ProductAddToCart


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.get("/")
def get_cart(db: db_dependency, session_id : str = Cookie(...)):
    return get_cart_products(db, session_id)

@router.post("/")
def add_to_cart(product: ProductAddToCart, db: db_dependency, session_id : str = Cookie(...)):
    return add_product_to_cart(product, db, session_id)