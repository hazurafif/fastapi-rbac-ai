from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from models.users import (
    LoginModel,
    Users
)
from routers import (
    users
)
import logging
import jwt

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

SECRET_KEY = "super-secret-key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@app.post("/login")
async def login(response: Response, login: LoginModel):
    user = Users.authenticate_user(login.email, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    ) 
     # Set the cookie token
    response.set_cookie(
        key="token",
        value=access_token,
        expires=access_token_expires,
        httponly=True,  # Ensures the cookie is not accessible via JavaScript
        samesite='lax',
        secure='lax',
    )
    return {
        "token": access_token,
            
    }

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])