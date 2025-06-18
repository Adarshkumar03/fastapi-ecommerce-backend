from sqlalchemy.orm import Session
from sqlalchemy import Column
from datetime import datetime, timezone
from typing import cast
from .schema import CartItemCreate, CartItemOut, CartItemUpdate

def create_cart_item(db: Session, item: CartItemCreate):
    print("Called!!")