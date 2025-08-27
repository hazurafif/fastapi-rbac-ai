from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.users import (
    LoginModel
)
from routers import (
    users
)
import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # allows all headers
)

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/login")
async def login(login: LoginModel):
    return login

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])