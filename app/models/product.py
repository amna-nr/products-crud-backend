from app.core.database import Base 
from sqlalchemy import Column, String, Integer 


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)