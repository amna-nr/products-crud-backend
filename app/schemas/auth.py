from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str
    confirm_password: str