from fastapi import APIRouter, Cookie
from app.services.checkout import create_checkout_session
from app.core.database import db_dependency


router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)

@router.post("/create-payment-session")
def payment_session(db: db_dependency, session_id: str | None = Cookie(None)):
    return create_checkout_session(db, session_id)
