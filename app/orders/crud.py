from sqlalchemy.orm import Session
from .models import Orders

def get_user_orders(db: Session, user_id: int):
    return db.query(Orders).filter(Orders.user_id == user_id).all()

def get_order_by_id(db: Session, user_id: int, order_id: int):
    return db.query(Orders).filter(Orders.user_id == user_id, Orders.id == order_id).first()