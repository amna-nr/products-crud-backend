import json

from datetime import datetime, timezone
from fastapi import Cookie, HTTPException
from sqlalchemy import select
from starlette import status
from uuid import UUID

from app.core.database import db_dependency
from app.core.redis import redis_client
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.products import ProductAddToCart


def get_cart_products(db: db_dependency, session_id : str = Cookie(...)):
    user = redis_client.get(f"session:{session_id}")
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in to access the cart"
        )
    user = json.loads(user)
    user_id = UUID(user["id"])
 
    result = db.execute(select(Cart).where(Cart.user_id == user_id).order_by(Cart.added_at.desc()))
    cart = result.scalars().all()

    products = []
    for cart_item in cart:
        result = db.execute(select(Product).where(Product.id == cart_item.product_id))
        product = result.scalar_one_or_none()
        products.append({"product" : product,
                        "quantity" : cart_item.quantity})
    return products


def add_product_to_cart(product: ProductAddToCart, db: db_dependency, session_id : str = Cookie(...)):
    user = redis_client.get(f"session:{session_id}")
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in to access the cart"
        )
    user = json.loads(user)
    user_id = UUID(user["id"])

    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product.id))
    existing_product = result.scalar_one_or_none()
    if existing_product: 
        existing_product.quantity += product.quantity
        existing_product.added_at = datetime.now(timezone.utc)
        db.commit()
    else:    
        new_product = Cart(user_id = user_id, product_id = product.id, quantity = product.quantity)
        db.add(new_product)
        db.commit()

    return {"message" : "Product has been added to cart"}
    