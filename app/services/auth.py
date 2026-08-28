from app.schemas.auth import UserRegister
from app.core.database import db_dependency
from app.core.security import hash_password
from app.models.user import User
from sqlalchemy import select
from fastapi import HTTPException
from starlette import status



async def register(credentials: UserRegister, db: db_dependency):
    if credentials.password != credentials.confirm_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail = "Passwords do not match"
            )
    
    result = await db.execute(select(User).where(User.email == credentials.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = "User already exists"
        )

    password_hash = hash_password(credentials.password)

    new_user = User(email=credentials.email, password_hash=password_hash)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message" : "user has been created"}