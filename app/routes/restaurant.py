from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from pydantic import BaseModel
from typing import List
from jose import jwt
from app.core.jwt import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# Clean Bearer token scheme for Swagger
bearer_scheme = HTTPBearer()

class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None
    address: str
    phone: str | None = None

class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: str | None
    address: str
    phone: str | None
    owner_id: int

    class Config:
        from_attributes = True

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

# CREATE Restaurant (role check temporary comment - testing ke liye)
@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Temporary comment - baad mein uncomment kar dena
    # if current_user.role != UserRole.restaurant_owner:
    #     raise HTTPException(status_code=403, detail="Only restaurant owners can create restaurants")

    new_restaurant = Restaurant(**restaurant.dict(), owner_id=current_user.id)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# READ All Restaurants (public - no token needed)
@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()

# READ Single Restaurant (public)
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant