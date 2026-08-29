from app.services.auth import register, login, logout
from app.schemas.auth import UserRegister, UserLogin
from app.core.database import db_dependency
from fastapi import APIRouter, Response, Cookie


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

@router.post("/logout")
async def logout_user(response: Response, session_id: str = Cookie(...)):
    return await logout(response, session_id)