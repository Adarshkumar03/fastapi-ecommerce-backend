from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.security import get_current_user
from .crud import process_checkout

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/")
async def checkout(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return process_checkout(db, user.id)