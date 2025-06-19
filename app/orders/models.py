from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from ..core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime, timezone
class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default=OrderStatus.PENDING.value)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    items = relationship("OrderItems", back_populates="order")
    
class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Orders", back_populates="items")
    product = relationship("Products", back_populates="order_items")    
