from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    meals = relationship("Meal", back_populates="owner")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    meal_type = Column(String, nullable=False)
    food_items = Column(String, nullable=False)  # Armazena itens como string separada por vírgula
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    owner = relationship("User", back_populates="meals")
