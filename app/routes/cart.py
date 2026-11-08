from uuid import UUID
from fastapi import APIRouter, Cookie
from app.core.database import db_dependency
from app.services.cart import get_cart_products, get_selected_cart_products
from app.services.cart import add_product_to_cart, delete_product_from_cart, update_cart_product, select_cart_product
from app.schemas.cart import CartProductUpdate
from app.schemas.products import ProductAddToCart


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.get("/")
def get_cart(db: db_dependency, session_id : str | None = Cookie(None)):
    return get_cart_products(db, session_id)

@router.get("/selected")
def get_selected_products(db: db_dependency, session_id : str | None = Cookie(None)):
    return get_selected_cart_products(db, session_id)

@router.post("/")
def add_to_cart(product: ProductAddToCart, db: db_dependency, session_id : str | None = Cookie(None)):
    return add_product_to_cart(product, db, session_id)

@router.put("/{product_id}")
def select_from_cart(product_id: int, db: db_dependency, session_id : str | None = Cookie(None)):
    return select_cart_product(product_id, db, session_id)

@router.delete("/{product_id}")
def delete_from_cart(product_id: int,  db: db_dependency, session_id : str | None = Cookie(None)):
    return delete_product_from_cart(product_id, db, session_id)

@router.put("/")
def update_cart(product: CartProductUpdate, db: db_dependency, session_id : str | None = Cookie(None)):
    return update_cart_product(product, db, session_id)