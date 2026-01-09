from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routes.restaurant import get_current_user  # same dependency
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

# All users dekhne ke liye (sirf logged in user dekh sake)
@router.get("/", response_model=List[UserResponse])
def get_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Single user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user