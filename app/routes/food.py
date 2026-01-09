from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.food import Food
from app.models.restaurant import Restaurant
from app.models.user import User
from app.routes.restaurant import get_current_user  # same dependency
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/food", tags=["Food Menu"])

class FoodCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class FoodResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    restaurant_id: int

    class Config:
        from_attributes = True

# Owner apne restaurant mein food item add kare
@router.post("/{restaurant_id}", response_model=FoodResponse)
def add_food_item(
    restaurant_id: int,
    food: FoodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if restaurant belongs to current user
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id).first()
    if not restaurant:
        raise HTTPException(status_code=403, detail="You can only add food to your own restaurant")

    new_food = Food(**food.dict(), restaurant_id=restaurant_id)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

# Restaurant ka menu browse (public - koi bhi dekh sake)
@router.get("/{restaurant_id}", response_model=List[FoodResponse])
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    items = db.query(Food).filter(Food.restaurant_id == restaurant_id).all()
    return items

# All food items (optional)
@router.get("/", response_model=List[FoodResponse])
def get_all_food(db: Session = Depends(get_db)):
    return db.query(Food).all()