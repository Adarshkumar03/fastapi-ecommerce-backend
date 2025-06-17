from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from ..core.database import Base
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(20), default=UserRole.USER.value)
    hashed_password = Column(String(128), nullable=False)

class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    expiration_time: Mapped[float] = mapped_column(nullable=False) 
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    
    