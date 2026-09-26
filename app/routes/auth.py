from app.services.auth import register, login, logout
from app.schemas.auth import UserRegister, UserLogin
from app.core.database import db_dependency
from fastapi import APIRouter, Response, Cookie


router = APIRouter(
    prefix= "/auth",
    tags=["auth"]
)


@router.post("/register")
def register_user(credentials: UserRegister, db: db_dependency):
    return register(credentials, db)

@router.post("/login")
def login_user(credentials: UserLogin, db: db_dependency, response: Response):
    return login(credentials, db, response)

@router.post("/logout")
def logout_user(response: Response, session_id: str = Cookie(...)):
    return logout(response, session_id)