from app.schemas.auth import UserRegister, UserLogin
from app.core.database import db_dependency
from app.core.security import hash_password, check_password, create_session
from app.models.user import User
from app.core.redis import redis_client

from sqlalchemy import select
from fastapi import HTTPException, Response, Cookie
from starlette import status


def register(credentials: UserRegister, db: db_dependency):
    if credentials.password != credentials.confirm_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid credentials"
            )
    
    result = db.execute(select(User).where(User.email == credentials.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = "Invalid credentials"
        )

    password_hash = hash_password(credentials.password)

    new_user = User(email=credentials.email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message" : "user has been created"}


def login(credentials: UserLogin, db: db_dependency, response: Response):
    result = db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if user is None:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid credentials"
          )

    if not check_password(credentials.password, user.password_hash):
         raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid credentials"
          )

    create_session(str(user.id), user.email, response)

    return {"message": "logged in"}
    

def logout(response: Response, session_id: str = Cookie(...)):
    session = redis_client.get(f"session:{session_id}")

    if not session:
        raise HTTPException(
             status_code=401, 
             detail="Session not found"
        )

    redis_client.delete(f"session:{session_id}")

    response.delete_cookie("session_id")

    return {"message": "User has been logged out"}


     