from sqlalchemy import Column, String, Integer, Boolean
from app.core.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4 )
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="member")
    is_verified = Column(Boolean, default=False)