import bcrypt
import jwt

from config_data.config import Config

auth_config = Config.authJWT


def encode_jwt(
        payload: dict,
        private_key: str = auth_config.private_key_path.read_text(),
        algorithm: str = auth_config.algorithm,
) -> str:
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = auth_config.public_key_path.read_text(),
        algorithm: str = auth_config.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
