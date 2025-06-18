from sqlalchemy.orm import Session
from ..cart.models import Cart
from ..orders.models import Orders, OrderItems
from ..products.models import Products

def process_checkout(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise ValueError("Cart is empty")

    total_amount = 0
    for item in cart_items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise ValueError("Product unavailable or out of stock")
        total_amount += product.price * item.quantity
        product.stock -= item.quantity  # Reduce stock

    order = Orders(user_id=user_id, total_amount=total_amount, status="paid")
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        if product is None:
            raise ValueError("Product not found during checkout")

        price_at_purchase = product.price
        order_item = OrderItems(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=price_at_purchase
        )
        db.add(order_item)

    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {"message": "Checkout successful", "order_id": order.id}
