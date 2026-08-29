from app.schemas.auth import UserRegister, UserLogin
from app.core.database import db_dependency
from app.core.security import hash_password, check_password, create_session
from app.models.user import User

from sqlalchemy import select
from fastapi import HTTPException, Response 
from starlette import status


async def register(credentials: UserRegister, db: db_dependency):
    if credentials.password != credentials.confirm_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid credentials"
            )
    
    result = await db.execute(select(User).where(User.email == credentials.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = "Invalid credentials"
        )

    password_hash = hash_password(credentials.password)

    new_user = User(email=credentials.email, password_hash=password_hash)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message" : "user has been created"}


async def login(credentials: UserLogin, db: db_dependency, response: Response):
    result = await db.execute(select(User).where(User.email == credentials.email))
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

    await create_session(str(user.id), user.email, response)

    return {"message": "logged in"}
    

    