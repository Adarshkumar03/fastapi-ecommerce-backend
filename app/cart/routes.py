from ..core.database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from ..auth.security import get_current_user
from .schema import CartItemCreate, CartItemOut, CartItemUpdate
from .crud import add_to_cart, get_cart_items, remove_from_cart, update_cart_item

router = APIRouter()

@router.post("/", response_model=CartItemOut)
async def add_product_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return add_to_cart(db, user.id, item)

@router.get("/", response_model=list[CartItemOut])
async def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_cart_items(db, user.id)

@router.delete("/{product_id}")
async def remove_product_from_cart(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return remove_from_cart(db, user.id, product_id)

@router.put("/{product_id}", response_model=CartItemOut)
async def update_product_quantity(product_id: int, item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_cart_item(db, user.id, product_id, item.quantity)