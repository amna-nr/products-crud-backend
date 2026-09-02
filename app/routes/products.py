from app.services.products import products_get, product_get_by_id, product_create, product_update, product_delete
from app.core.database import db_dependency
from app.schemas.products import ProductCreate, ProductUpdate
from fastapi import APIRouter


router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
async def get_products(db: db_dependency):
    return await products_get(db)

@router.get("/{id}")
async def get_product_by_id(db: db_dependency, id: int):
    return await product_get_by_id(db, id)

@router.post("/")
async def create_product(db: db_dependency, product_details: ProductCreate):
    return await product_create(db, product_details)

@router.put("/{id}")
async def update_product(db: db_dependency, product_id: int, product_details: ProductUpdate):
    return await product_update(db, product_id, product_details)

@router.delete("/{id}")
async def delete_product(db: db_dependency, id: int):
    return await product_delete(db, id)
