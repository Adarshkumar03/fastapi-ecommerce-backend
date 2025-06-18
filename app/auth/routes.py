from ..core.database import get_db
from .utils import check_password, send_reset_email, generate_password_hash
from .crud import create_user, get_all_users, get_user_by_email, create_password_reset_token, is_token_valid, mark_token_as_used, get_user_by_username
from .schema import UserCreate, UserOut, ResetPasswordRequest
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .security import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .models import User, PasswordResetTokens

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
    db_user =  get_user_by_username(db, form_data.username)
    print(f"DB User: {db_user}")
    if not db_user:
        raise HTTPException(status_code=404, detail={"message": "User not found", "error":"True", "status_code": 404})
    if check_password(db_user.hashed_password, form_data.password):
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": db_user.email},
            expires_delta=access_token_expires
        )
        refresh_token_expires = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        refresh_token = create_access_token(
            data={"sub": db_user.email},
            expires_delta=refresh_token_expires
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
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

@router.post("/forget-password")
async def forget_password(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail={"message": "User not found", "error":"True", "status_code": 404})
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=15)
    )
    create_password_reset_token(
        db=db,
        user_id=user.id,
        token=token,
        expiration_time=(datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()
    )
    send_reset_email(
        subject="Reset Password",
        body="Here is the token to reset your password.  Please use it within the next 15 minutes.",
        token=token,
        recipient_email=str(user.email)
    )
    return {"message": "Password reset email sent", "error": "False", "status_code": 200}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    token = request.token
    new_password = request.new_password
    if not new_password:
        raise HTTPException(status_code=400, detail={"message": "New password is required", "error": "True", "status_code": 400})
    if not is_token_valid(db, token):
        raise HTTPException(status_code=400, detail={"message": "Invalid or expired token", "error": "True", "status_code": 400})
    
    reset_token = db.query(PasswordResetTokens).filter(PasswordResetTokens.token == token).first()
    if not reset_token:
        raise HTTPException(status_code=404, detail={"message": "Token not found", "error": "True", "status_code": 404})

    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail={"message": "User not found", "error": "True", "status_code": 404})
    setattr(user, "hashed_password", generate_password_hash(new_password))
    db.commit()
    db.refresh(user)
    mark_token_as_used(db, token)
    return {"message": "Password reset successful", "error": "False", "status_code": 200}