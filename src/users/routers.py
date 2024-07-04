from fastapi import APIRouter, Depends, HTTPException

from config_data.config import Config, load_config
from src.users.schemas import UserCreate, Token, UserLogin
from src.users.services import UserService
from src.utils.auth_settings import encode_jwt

router = APIRouter(tags=["user"], prefix="/user")

settings: Config = load_config(".env")
auth_config = settings.authJWT


@router.post("/register")
async def register(user_create: UserCreate) -> Token:
    user = await UserService().create_user(user_create)
    access_token = encode_jwt(payload={"sub": user.short_name})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def authenticate_user_jwt(user: UserLogin = Depends(UserService.authenticate_user)):
    jwt_payload = {
        "sub": user.short_name,
        "short_name": user.short_name,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer"
    )
