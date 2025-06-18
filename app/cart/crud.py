from sqlalchemy.orm import Session
from sqlalchemy import Column
from datetime import datetime, timezone
from typing import cast
from .schema import CartItemCreate, CartItemOut, CartItemUpdate
from .models import Cart
from ..products.models import Products

def add_to_cart(db: Session, user_id: int, item: CartItemCreate):
    product = db.query(Products).filter(Products.id == item.product_id).first()
    if not product:
        raise ValueError("Product does not exist")
    
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart_items(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not cart_item:
        raise ValueError("Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not cart_item:
        raise ValueError("Cart item not found")
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item