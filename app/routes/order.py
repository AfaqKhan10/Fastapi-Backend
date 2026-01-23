from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.food import Food
from app.models.restaurant import Restaurant
from app.models.user import User
from app.routes.restaurant import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])


class OrderItemCreate(BaseModel):
    food_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    address: str
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    restaurant_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    address: str

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: OrderStatus

# Customer order place kare
@router.post("/", response_model=OrderResponse)
def place_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_price = 0
    order_items = []

    for item in order.items:
        food = db.query(Food).filter(Food.id == item.food_id, Food.restaurant_id == order.restaurant_id).first()
        if not food:
            raise HTTPException(status_code=404, detail=f"Food item with id {item.food_id} not found in this restaurant")
        item_total = food.price * item.quantity
        total_price += item_total
        order_items.append(OrderItem(food_id=item.food_id, quantity=item.quantity, price_at_time=food.price))

    new_order = Order(
        customer_id=current_user.id,
        restaurant_id=order.restaurant_id,
        total_price=total_price,
        address=order.address
    )
    db.add(new_order)
    db.flush()

    for oi in order_items:
        oi.order_id = new_order.id
        db.add(oi)

    db.commit()
    db.refresh(new_order)
    return new_order

# Customer apne orders dekhe
@router.get("/my-orders", response_model=List[OrderResponse])
def my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.customer_id == current_user.id).all()

# Koi bhi restaurant ke orders dekh sake (testing ke liye owner check comment)
@router.get("/restaurant/{restaurant_id}", response_model=List[OrderResponse])
def restaurant_orders(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Owner check comment kar diya — testing ke liye koi bhi dekh sake
    # restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id).first()
    # if not restaurant:
    #     raise HTTPException(status_code=403, detail="Not your restaurant")

    return db.query(Order).filter(Order.restaurant_id == restaurant_id).all()

# Koi bhi status update kar sake (testing ke liye owner check comment)
@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: StatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Owner check comment kar diya — testing ke liye koi bhi update kar sake
    # restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id, Restaurant.owner_id == current_user.id).first()
    # if not restaurant:
    #     raise HTTPException(status_code=403, detail="Not authorized to update this order")

    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order


    # Customer apna pending order cancel (delete) kar sake
@router.delete("/{order_id}", response_model=dict)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id, Order.customer_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not yours")

    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")

    # Order items bhi delete ho jayenge cascade se (agar set hai)
    db.delete(order)
    db.commit()

    return {"message": "Order cancelled successfully"}
