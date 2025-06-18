from ..core.database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from ..auth.security import user_required
from .schema import CartItemCreate
from .crud import create_cart_item

router = APIRouter()

@router.post("/", dependencies=[Depends(user_required)])
async def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    create_cart_item(db, item)