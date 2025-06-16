from app.auth.schema import UserCreate
from .models import UserInDB
from sqlalchemy.orm import Session
from .utils import generate_password_hash
from .models import UserInDB

def create_user(db: Session, user: UserCreate) -> UserCreate:
    """
    Create a new user in the database.
    """
    if not db:
        raise ValueError("Database session is not available")
    hashed_password = generate_password_hash(user.password)
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already exists")

    db_user = UserInDB(
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
    users = db.query(UserInDB).all()
    if not users:
        raise ValueError("No users found")
    return users

def get_user_by_email(db: Session, email: str) -> UserInDB:
    """
    Retrieve a user by email from the database.
    """
    user = db.query(UserInDB).filter(UserInDB.email == email).first()
    if not user:
        raise ValueError("User not found")
    return user