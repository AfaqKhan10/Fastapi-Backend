from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

# Payment status alag enum — isliye "paid" error nahi aayega
class PaymentStatus(enum.Enum):
    unpaid = "unpaid"
    paid = "paid"
    failed = "failed"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    # payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.unpaid)  # ← NAYA COLUMN
    created_at = Column(DateTime, default=datetime.utcnow)
    address = Column(String, nullable=False)

    customer = relationship("User")
    restaurant = relationship("Restaurant")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    food = relationship("Food")