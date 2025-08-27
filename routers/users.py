from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    return

@router.post("/add")
async def create_users():
    return

@router.delete("/delete")
async def delete_users():
    return

@router.put("/")
async def update_users():
    return