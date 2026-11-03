from fastapi import APIRouter, Cookie
from app.services.checkout import create_checkout_session
from app.core.database import db_dependency
from app.services.cart import manage_stock

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)

@router.post("/create-payment-session")
def payment_session(db: db_dependency, session_id: str = Cookie(...)):
    return create_checkout_session(db, session_id)

@router.post("/payment-success")
def payment_success(db: db_dependency, session_id: str = Cookie(...)):
    products = manage_stock(db, session_id)
    return products