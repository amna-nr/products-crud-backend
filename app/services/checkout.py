from app.core.stripe import client
from app.services.images import get_image
from app.core.database import db_dependency
from app.services.cart import get_products, get_selected_cart_products
from fastapi import Cookie, HTTPException
from starlette import status

def create_checkout_session(db: db_dependency, session_id : str = Cookie(...)):
    selected_products = get_selected_cart_products(db, session_id)
    products = get_products(selected_products, db)

    if not products: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    line_items = []

    for product_info in products:
        product_data = {"name": product_info["product"].name}

        image_url = get_image(product_info["product"].name)
        if image_url:
            product_data["images"] = [image_url]

        line_items.append({
            "price_data": {
                "currency": "pkr",
                "product_data": product_data,
                "unit_amount": int(product_info["product"].price * 100)
            },
            "quantity": product_info["quantity"],
        })

    session = client.v1.checkout.sessions.create({
        "success_url": "http://localhost:5173/payment-success",
        "line_items": line_items,
        "mode": "payment",
    })
    return session.url