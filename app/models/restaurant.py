from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String, nullable=False)
    phone = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relations
    owner = relationship("User", back_populates="restaurants")
    foods = relationship("Food", back_populates="restaurant", cascade="all, delete")