from app.services.products import products_get, product_get_by_id, product_create, product_update, product_delete
from app.core.database import db_dependency
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from fastapi import APIRouter


router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_products(db: db_dependency):
    return products_get(db)

@router.get("/{id}")
def get_product_by_id(db: db_dependency, id: int):
    return product_get_by_id(db, id)

@router.post("/")
def create_product(db: db_dependency, product_details: ProductCreate) -> ProductResponse:
    return product_create(db, product_details)

@router.put("/{id}")
def update_product(db: db_dependency, id: int, product_details: ProductUpdate):
    return product_update(db, id, product_details)

@router.delete("/{id}")
def delete_product(db: db_dependency, id: int):
    return product_delete(db, id)
