from pydantic import BaseModel, EmailStr, constr

# User registration request
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response model
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
