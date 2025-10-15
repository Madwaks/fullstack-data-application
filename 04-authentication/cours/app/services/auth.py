import base64
import hashlib
import hmac
import os
from typing import Dict, Union, List

import jwt
from fastapi import HTTPException, Header
from sqlalchemy.orm import Session

import models
from exceptions.user import UserNotFound, IncorrectPassword
from serializers import User

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")


def _encode_jwt(user: User) -> str:
    return jwt.encode(
        {
            "user_id": str(user.id),
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )

def decode_jwt(token: str) -> User:
    try:
        auth = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_SECRET_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=f"Invalid token: '{err}'")

    return auth

def generate_access_token(
    db: Session,
    user_login: User,
):
    password = user_login.password

    user = (
        db.query(models.User)
        .filter(
            models.User.username == user_login.username,
        )
        .first()
    )

    if not user:
        raise UserNotFound

    if not check_password(password, user.password):
        raise IncorrectPassword

    return _encode_jwt(user)

def hash_password(password: str, iterations: int = 600_000) -> str:
    # Generate a random 16-byte salt
    salt = os.urandom(16)
    # Derive the hash using PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    # Encode salt and hash in base64 for safe storage
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    hash_b64 = base64.b64encode(dk).decode('utf-8')
    # Return full formatted hash string
    return f"pbkdf2_sha256${iterations}${salt_b64}${hash_b64}"


def check_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored_hash.split('$')
    except Exception:
        raise ValueError("Invalid hash format")

    iterations = int(iterations)
    salt = base64.b64decode(salt_b64)
    stored_dk = base64.b64decode(hash_b64)

    new_dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)

    return hmac.compare_digest(stored_dk, new_dk)
