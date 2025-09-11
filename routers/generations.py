from fastapi import APIRouter, HTTPException
from models.generations import (
    GenerationModel,
    Generations
)
router = APIRouter()

@router.get("/")
async def get_generations():
    return
