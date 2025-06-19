from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from .schema import OrderOut
from .crud import get_user_orders, get_order_by_id
from ..auth.security import get_current_user
from ..auth.models import User
from typing import List

router = APIRouter()

@router.get("/", response_model=List[OrderOut])
async def view_order_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = get_user_orders(db, current_user.id) # type: ignore
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user.")
    return orders

@router.get("/{order_id}", response_model=OrderOut)
async def view_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = get_order_by_id(db, current_user.id, order_id) # type: ignore
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order
