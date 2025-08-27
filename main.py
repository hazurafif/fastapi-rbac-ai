from fastapi import FastAPI
from models.users import (
    LoginModel
)
from routers import (
    users
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/login")
async def login(login: LoginModel):
    return login

app.include_router(users.router, prefix="/users", tags=["users"])