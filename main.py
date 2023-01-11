import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user import router as user_routers
from routers.auth import router as auth_routers

from dotenv import load_dotenv

load_dotenv("e_commerce/.env")

app = FastAPI(title="Restaurant CRM", openapi_url="/api/openapi.json")

origins = [
    os.environ["CLIENT_ORIGIN"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_routers, tags=["Users"], prefix="/api/users")
app.include_router(auth_routers, tags=["Auth"], prefix="/api/auth")


@app.get("/api/healthchecker")
def root():
    return {"message": "ok"}
