import jwt
import time
from app.config import SECRET_KEY, JWT_ISSUER, EXPIRY_TOKEN
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.storage import get_user_by_id, get_user_by_name
from app.security import verify_password
from app.exceptions import InvalidCredentials, UserNotFound
from typing import Annotated

# to take a token, refer to the login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(payload: dict) -> dict:
    payload_copy = payload.copy()
    payload_copy["iat"] = int(time.time())
    payload_copy["exp"] = payload_copy["iat"] +  EXPIRY_TOKEN
    payload_copy["iss"] = JWT_ISSUER

    return {
        "access_token": jwt.encode(payload_copy, SECRET_KEY, algorithm="HS256"),
        "token_type": "bearer"
    }

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, issuer=JWT_ISSUER, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise InvalidCredentials
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = verify_token(token)
        return get_user_by_id(payload["sub"])
    except UserNotFound, InvalidCredentials:
        raise InvalidCredentials

def authenticate_user(username: str, password: str):
    try:
        user = get_user_by_name(username)
    except UserNotFound:
        raise InvalidCredentials
    
    if not verify_password(password, user.hashed_password):
        # invalid password or username doesnt exist
        raise InvalidCredentials
    
    return user
    
