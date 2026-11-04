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

def get_selected_cart_products (db: db_dependency, session_id: str = Cookie(...)):
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
        products.append({"product" : product,
                        "quantity" : cart_item.quantity,
                        "is_selected": cart_item.is_selected})
    return products

def get_cart_products(db: db_dependency, session_id : str = Cookie(...)):
    user_id = get_user(session_id)

    result = db.execute(select(Cart).where(Cart.user_id == user_id).order_by(Cart.added_at.desc()))
    cart = result.scalars().all()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your cart is empty"
        )
    
    return get_products(cart, db)

def add_product_to_cart(product: ProductAddToCart, db: db_dependency, session_id : str = Cookie(...)):
    user_id = get_user(session_id)

    result = db.execute(select(Product).where(Product.id == product.id))
    existing_product = result.scalar_one_or_none()

    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product does not exist")

    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product.id))
    cart_product = result.scalar_one_or_none()

    if existing_product.stock_quantity - product.quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock limit exceeded"
        )
    if product.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Add one or more products"
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

def delete_product_from_cart(product_id: int, db: db_dependency, session_id : str = Cookie(...)):
    user_id = get_user(session_id)

    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
    cart_product = result.scalar_one_or_none() 

    if not cart_product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    result = db.execute(delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
    db.commit() 
    return {"message" : "Product removed from cart"}

def update_cart_product(product: CartProductUpdate, db: db_dependency, session_id : str = Cookie(...)):
    user_id = get_user(session_id)
        
    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product.id))
    cart_product = result.scalar_one_or_none()

    if not cart_product: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")

    result = db.execute(select(Product).where(Product.id == product.id))
    existing_product = result.scalar_one_or_none()

    if product.quantity > cart_product.quantity:
        if existing_product.stock_quantity - product.quantity >= 0: 
            cart_product.quantity = product.quantity
    if product.quantity < cart_product.quantity and cart_product.quantity > 1: 
        cart_product.quantity = product.quantity

    db.commit()
    db.refresh(cart_product)
    
    return {"message" : "Product edited in cart"}

def select_cart_product(product_id: int, db: db_dependency, session_id : str = Cookie(...)):
    user_id = get_user(session_id)
        
    result = db.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
    cart_product = result.scalar_one_or_none()

    if not cart_product: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")

    cart_product.is_selected = not cart_product.is_selected

    db.commit()
    db.refresh(cart_product)
    
    return {"message" : "Product edited in cart"}

def manage_stock(db: db_dependency, session_id : str = Cookie(...)):
    selected_products = get_selected_cart_products(db, session_id)
    for selected_product in selected_products: 
        result = db.execute(select(Product).where(Product.id == selected_product.product_id))
        product = result.scalar_one_or_none()
        product.stock_quantity = product.stock_quantity - selected_product.quantity
        db.commit()
    return selected_products
        
