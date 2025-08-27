from fastapi import APIRouter, HTTPException
from models.users import (
    UserRegistrationModel,
    Users
)
router = APIRouter()

@router.get("/")
async def get_users():
    return

@router.post("/add")
async def create_users(form: UserRegistrationModel):
    user = Users.insert_new_user(form)
    if not user: 
        raise HTTPException(400)
    return user

@router.delete("{id}/delete")
async def delete_users():
    return

@router.put("/update")
async def update_users():
    return