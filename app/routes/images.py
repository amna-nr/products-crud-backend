from app.services.images import get_image
from fastapi import APIRouter


router = APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.get("/{product}")
def get_unsplash_image(product: str):
    return get_image(product)
