from app.core.config import settings
import requests 


def get_image (product: str):
    response = requests.get("https://api.unsplash.com/search/photos", 
                headers={
                    "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"
                },
                params={
                    "query": product
                })
    url = response.json()["results"][0]["urls"]["thumb"]
    return url