import requests
from app.core.config import settings


def get_image (product: str):
    response = requests.get(f"{settings.UNSPLASH_API_URL}",
                headers={
                    "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"
                },
                params={
                    "query": product
                })
    url = response.json()["results"][0]["urls"]["thumb"]
    return url
