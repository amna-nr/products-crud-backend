from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.product import Product
from app.models.user import User


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey(User.id))
    product_id = Column(Integer, ForeignKey(Product.id))
    quantity = Column(Integer)