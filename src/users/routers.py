from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from config_data.config import Config, load_config
from src.reports.services import ReportService
from src.users.models import User
from src.users.schemas import UserCreate, Token, UserLogin, UserResponse
from src.users.services import UserService
from src.utils.auth_settings import encode_jwt

router = APIRouter(tags=["user"], prefix="/user")

settings: Config = load_config(".env")
auth_config = settings.authJWT


@router.post("/register")
async def register(user_create: UserCreate) -> Token:
    user = await UserService().create_user(user_create)
    access_token = encode_jwt(payload={"sub": user.short_name})
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/login", response_model=Token)
async def authenticate_user_jwt(user: UserLogin = Depends(UserService().authenticate_user)) -> Token:
    jwt_payload = {
        "sub": user.short_name,
        "short_name": user.short_name,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return Token(access_token=token, token_type="Bearer")


@router.get("/self")
async def login_for_access_token(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    return {
        "data": UserResponse(**current_user.to_dict()),
        "reports": ReportService().reports_to_dict(current_user.reports)
    }


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user = await UserService().get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "data": UserResponse(**user.to_dict()),
        "reports": ReportService().reports_to_dict(user.reports)
    }


@router.delete("")
async def delete_user(
        current_user: Annotated[User, Depends(UserService().get_current_user)]
):
    await UserService().delete_user(current_user)
    return {"success": "ok"}
