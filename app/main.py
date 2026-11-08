from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.cart import router as cart_router
from app.routes.images import router as images_router
from app.routes.products import router as products_router
from app.routes.checkout import router as payment_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(images_router)
app.include_router(products_router)
app.include_router(payment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def homepage():
    return {"message" : "Welcome!"}
