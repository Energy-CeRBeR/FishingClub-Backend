import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config_data.config import Config, load_config
from src.users.models import User
from src.users.repositories import UserRepository
from src.users.schemas import UserCreate, TokenData
from src.utils.auth_settings import validate_password, decode_jwt

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
http_bearer = HTTPBearer()

settings: Config = load_config(".env")
auth_config = settings.authJWT


class UserService:
    repository = UserRepository()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await self.repository.get_user_by_email(email)
        if not user:
            raise credentials_exception
        if not validate_password(password, user.password_hash):
            raise credentials_exception

        return user

    async def authenticate_user_by_token(self, token: str) -> User | None:
        pass

    async def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token = token.credentials
            print("TOKEN:", token)
            payload = decode_jwt(token=token)
            short_name: str = payload.get("sub")
            print("NAME:", short_name)
            if short_name is None:
                raise credentials_exception
            token_data = TokenData(short_name=short_name)
        except jwt.DecodeError:
            print("E1")
            raise credentials_exception
        except jwt.ExpiredSignatureError:
            print("E2")
            raise credentials_exception
        user = await self.repository.get_user_by_short_name(token_data.short_name)
        if user is None:
            print("E3")
            raise credentials_exception

        return user

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    async def create_user(self, user: UserCreate) -> User:
        return await self.repository.create_user(user)

    async def delete_user(self, user: User) -> None:
        return await self.repository.delete_user(user)
