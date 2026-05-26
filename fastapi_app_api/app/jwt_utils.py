from datetime import timedelta

from fastapi import HTTPException
from jose import jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id:int) -> str:
    payload = {"sub": str(user_id), "exp": settings.ACCESS_TOKEN_EXPIRE_MINUTES}
    jwt_token = jwt.encode(payload, settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return jwt_token

def create_refresh_token(user_id:int) -> str:
    payload = {"sub": str(user_id), "exp": settings.ACCESS_TOKEN_EXPIRE_MINUTES, "type": "refresh"}
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_token

def decode_token(token) -> dict | None:
    try:
        print(settings.SECRET_KEY)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except Exception as e:
        print(repr(e))
    # try:
    #     print(repr(token))
    #     token.strip().strip("'").replace("'", '')
    #     print(repr(token))
    #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #     if payload is None:
    #         raise HTTPException(status_code=401,detail="Invalid token")
    #     print(payload)
    #     return payload
    # except Exception as e:
    #     print('error in decoding token',repr(e))


