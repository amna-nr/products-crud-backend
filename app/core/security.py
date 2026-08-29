import bcrypt 
import secrets
import json
from app.core.redis import redis_client
from app.core.config import settings 
from fastapi import Response


def hash_password(password: str): 
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


async def create_session(user_id: str, user_email: str, response: Response):
    session_id = secrets.token_urlsafe()

    user = {
            "id" : user_id,
            "email": user_email
    }


    await redis_client.set(
            f"session:{session_id}",
            json.dumps(user),
            ex=3600,
        )

    response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=3600,
        )
