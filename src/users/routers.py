from fastapi import APIRouter, Depends, HTTPException

from src.users.schemas import UserCreate

router = APIRouter(tags=["user"], prefix="/user")


@router.post("/register")
async def register(user: UserCreate):
    pass
