import hashlib
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.settings import settings

oauth2_scheme = HTTPBearer()

# ----------------------
# PASSWORD HASHING (SHA256 + random salt)
# ----------------------
def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    salt = os.urandom(16).hex()        # 16-byte random salt
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"          # store salt + hash


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split("$")
        check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return hashed == check_hash
    except:
        return False


# ----------------------
# JWT helpers
# ----------------------
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {**data, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


# ----------------------
# Auth dependency
# ----------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    return payload
