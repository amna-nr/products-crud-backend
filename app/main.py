from fastapi import FastAPI
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(auth_router)


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