from fastapi import APIRouter
from app.services.images import get_image


router = APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.get("/{product}")
def get_unsplash_image(product: str):
    return get_image(product)
