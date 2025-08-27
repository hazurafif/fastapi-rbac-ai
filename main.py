from fastapi import FastAPI
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

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/login")
async def login(login: LoginModel):
    return login

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])