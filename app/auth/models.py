from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from ..core.database import Base
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(20), default=UserRole.USER.value)     

class UserInDB(Users):
    hashed_password = Column(String(128), nullable=False)

class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(128), unique=True, nullable=False)
    expiration_time = Column(Integer, nullable=False)
    used = Column(Boolean, default=False)
    
    