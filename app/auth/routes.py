from ..core.database import get_db
from .utils import check_password
from .crud import create_user, get_all_users, get_user_by_email
from .schema import UserCreate, UserOut
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .security import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session

from typing import Annotated

router = APIRouter()

#test route to check if the router is working
@router.get("/test/users", response_model=list[UserOut])
async def get_users(db:  Annotated[Session, Depends(get_db)]):
    users = get_all_users(db)
    return users

@router.post("/signin", response_model=Token)
async def signin_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Searches the database for a user with the provided credentials.
    If the user is found, returns the JWT access token for authentication.
    """
    db_user =  get_user_by_email(db, form_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail={"message": "User not found", "error":"True", "status_code": 404})
    if check_password(db_user.hashed_password, form_data.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email},
            expires_delta=access_token_expires
        )
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
    raise HTTPException(status_code=401, detail={"message": "Invalid password", "error":"True", "status_code": 401})

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(db, user)
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail={"message": str(ve), "error": "True", "status_code": 400}
        )
    return created_user



