from app.auth.schema import UserCreate
from .models import User
from sqlalchemy.orm import Session
from sqlalchemy import Column
from .utils import generate_password_hash
from datetime import datetime, timezone
from typing import cast

def create_user(db: Session, user: UserCreate) -> UserCreate:
    """
    Create a new user in the database.
    """
    hashed_password = generate_password_hash(user.password)
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role or "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_all_users(db: Session):
    """
    Retrieve all users from the database.
    """
    users = db.query(User).all()
    if not users:
        raise ValueError("No users found")
    return users

def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by email from the database.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username from the database.
    """
    return db.query(User).filter(User.username == username).first()

def create_password_reset_token(db: Session, user_id: Column[int], token: str, expiration_time: float):
    """
    Create a password reset token for a user.
    """
    from .models import PasswordResetTokens
    
    reset_token = PasswordResetTokens(
        user_id=user_id,
        token=token,
        expiration_time=expiration_time
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    
def is_token_valid(db: Session, token: str) -> bool:
    """
    Check if a password reset token is valid (not used and not expired).
    """
    from .models import PasswordResetTokens
    reset_token = db.query(PasswordResetTokens).filter(PasswordResetTokens.token == token).first()
    if not reset_token:
        print("Token not found")
        return False
    if reset_token.expiration_time < datetime.now(timezone.utc).timestamp():
        print("Token has expired")
        return False
    if not reset_token.used:
        return True
    print("Token has already been used")
    return False

def mark_token_as_used(db: Session, token: str):
    """
    Mark a password reset token as used.
    """
    from .models import PasswordResetTokens
    reset_token = db.query(PasswordResetTokens).filter(PasswordResetTokens.token == token).first()
    if not reset_token:
        raise ValueError("Token not found")
    reset_token.used = cast(bool, True)
    db.commit()
    db.refresh(reset_token)