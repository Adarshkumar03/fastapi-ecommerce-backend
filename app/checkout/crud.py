from sqlalchemy.orm import Session
from sqlalchemy import select
from app.products.models import Products
from app.cart.models import Cart
from app.orders.models import Orders, OrderItems
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError


def process_checkout(db: Session, user_id: int):
    try:
        cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
        if not cart_items:
            raise ValueError("Cart is empty")

        total_amount = 0

        for item in cart_items:
            product = db.query(Products).filter(Products.id == item.product_id).with_for_update().first()
            if not product:
                raise ValueError("Product not found")
            if product.stock < item.quantity:
                raise ValueError(f"Product '{product.name}' is out of stock or insufficient quantity")
            total_amount += product.price * item.quantity
            product.stock -= item.quantity

        order = Orders(
            user_id=user_id,
            total_amount=total_amount,
            status="paid",
            created_at=datetime.now(timezone.utc)
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        for item in cart_items:
            product = db.query(Products).filter(Products.id == item.product_id).first()
            if not product:
                raise ValueError("Product not found during order item creation")

            order_item = OrderItems(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
            db.add(order_item)

        db.query(Cart).filter(Cart.user_id == user_id).delete()
        db.commit()

        return {
            "error": False,
            "message": "Checkout successful",
            "order_id": order.id,
            "total_amount": total_amount,
            "code": 200
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError("Database error during checkout") from e
    except Exception as e:
        db.rollback()
        raise e
