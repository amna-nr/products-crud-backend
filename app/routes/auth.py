from app.services.auth import register
from app.schemas.auth import UserRegister
from app.core.database import db_dependency
from fastapi import APIRouter


router = APIRouter(
    prefix= "/auth",
    tags=["auth"]
)


@router.post("/register")
async def register_user(credentials: UserRegister, db: db_dependency):
    return await register(credentials, db)
    