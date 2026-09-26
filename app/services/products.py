from app.core.database import db_dependency
from app.models.product import Product
from app.schemas.products import ProductCreate, ProductUpdate
from sqlalchemy import select, delete
from fastapi import HTTPException
from starlette import status


def products_get(db: db_dependency):
    result = db.execute(select(Product))
    products = result.scalars().all()

    return products 

def product_get_by_id(db: db_dependency, product_id: int):
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product is None:
            raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail="Product not found"
            )

    return product

def product_create (db: db_dependency, product: ProductCreate):
    new_product = Product(name=product.name, price=product.price, quantity=product.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def product_update (db: db_dependency, product_id: int, product_details: ProductUpdate):
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    product.name = product_details.name 
    product.price = product_details.price
    product.quantity = product_details.quantity

    db.commit()
    db.refresh(product)

    return product

def product_delete (db: db_dependency, product_id: int):
    result = db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.execute(delete(Product).where(Product.id == product_id))
    db.commit()

    return {"message" : "Product has been deleted"}
