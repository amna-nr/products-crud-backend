import json

from datetime import datetime, timezone
from fastapi import Cookie, HTTPException
from sqlalchemy import select, delete
from starlette import status
from uuid import UUID

from app.core.database import db_dependency
from app.core.redis import redis_client
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.cart import CartProductUpdate
from app.schemas.products import ProductAddToCart


def get_user(session_id : str):
    user = redis_client.getex(f"session:{session_id}", ex=3600)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in"
        )
    user = json.loads(user)
    user_id = UUID(user["id"])
    return user_id

def get_selected_cart_products (db: db_dependency, session_id: str | None = Cookie(None)):
    user_id = get_user(session_id)
    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.is_selected == True))
    selected_products = result.scalars().all()

    if not selected_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products selected"
        )
 
    return selected_products

def get_products(cart: list, db: db_dependency):
    products = []
    for cart_item in cart:
        result = db.execute(select(Product).where(Product.id == cart_item.product_id))
        product = result.scalar_one_or_none()
        if not product: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        products.append({"product" : product,
                        "quantity" : cart_item.quantity,
                        "is_selected": cart_item.is_selected})
    return products

def get_cart_product(user_id: UUID, product_id: int, db: db_dependency):
    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
    cart_product = result.scalar_one_or_none() 
    
    if not cart_product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return cart_product




def get_cart_products(db: db_dependency, session_id : str | None = Cookie(None)):
    user_id = get_user(session_id)

    result = db.execute(select(Cart).where(Cart.user_id == user_id).order_by(Cart.added_at.desc()))
    cart = result.scalars().all()

    if not cart:
        return []
    return get_products(cart, db)

def add_product_to_cart(product: ProductAddToCart, db: db_dependency, session_id : str | None = Cookie(None)):
    user_id = get_user(session_id)

    result = db.execute(select(Product).where(Product.id == product.id))
    existing_product = result.scalar_one_or_none()

    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product does not exist"
        )

    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product.id))
    cart_product = result.scalar_one_or_none()

    if product.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Add one or more products"
            )
    if existing_product.stock_quantity - product.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock limit exceeded"
        )
    if  cart_product: 
        if cart_product.quantity + product.quantity >= existing_product.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Stock limit exceeded"
            )
        cart_product.quantity += product.quantity
        cart_product.added_at = datetime.now(timezone.utc)
        db.commit()
    else:    
        new_product = Cart(user_id = user_id, product_id = product.id, quantity = product.quantity)
        db.add(new_product)
        db.commit()
    return {"message" : "Product has been added to cart"}

def delete_product_from_cart(product_id: int, db: db_dependency, session_id : str | None = Cookie(None)):
    user_id = get_user(session_id)

    get_cart_product(user_id, product_id, db)

    db.execute(delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
    db.commit() 
    return {"message" : "Product removed from cart"}

def update_cart_product(product: CartProductUpdate, db: db_dependency, session_id : str | None = Cookie(None)):
    user_id = get_user(session_id)       
    cart_product = get_cart_product(user_id, product.id, db)

    result = db.execute(select(Product).where(Product.id == product.id))
    existing_product = result.scalar_one_or_none()

    if not existing_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.quantity < 1:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Quantity must be at least 1"
        )
    if product.quantity > existing_product.stock_quantity:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Stock limit exceeded"
        )
    
    cart_product.quantity = product.quantity
    db.commit()
    db.refresh(cart_product)
    
    return {"message" : "Product edited in cart"}

def select_cart_product(product_id: int, db: db_dependency, session_id : str | None = Cookie(None)):
    user_id = get_user(session_id)
        
    cart_product = get_cart_product(user_id, product_id, db)

    cart_product.is_selected = not cart_product.is_selected

    db.commit()
    db.refresh(cart_product)
    
    return {"message" : "Product edited in cart"}
