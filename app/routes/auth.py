from app.services.auth import register, login
from app.schemas.auth import UserRegister, UserLogin
from app.core.database import db_dependency
from fastapi import APIRouter, Response


router = APIRouter(
    prefix= "/auth",
    tags=["auth"]
)


@router.post("/register")
async def register_user(credentials: UserRegister, db: db_dependency):
    return await register(credentials, db)

@router.post("/login")
async def login_user(credentials: UserLogin, db: db_dependency, response: Response):
    return await login(credentials, db, response)
