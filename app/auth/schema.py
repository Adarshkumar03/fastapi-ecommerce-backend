from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.user
    
class LoginUser(BaseModel):
    email: str
    password: str    
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        orm_mode = True

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

