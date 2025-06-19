from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
import jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from typing import Annotated
from ..core.database import get_db
from .crud import get_user_by_email
from .models import User
from typing import Optional
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

class TokenData(BaseModel):
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": True,
            "message": "Could not validate credentials",
            "code": 401
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not ALGORITHM:
            raise HTTPException(status_code=500,detail={
                    "error": True,
                    "message": "JWT ALGORITHM is not set in environment variables",
                    "code": 500
                })
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    if not db:
        raise HTTPException(status_code=500, detail={
                "error": True,
                "message": "Database connection failed",
                "code": 500
            })
    if token_data.email is None:
        raise credentials_exception
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user

def admin_required(user: User = Depends(get_current_user)):
    if str(user.role) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": True,
                "message": "You do not have permission to perform this action.",
                "code": 403
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def user_required(user: User = Depends(get_current_user)):
    if str(user.role) != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": True,
                "message": "Only users have permission",
                "code": 403
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user