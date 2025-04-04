from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class MealBase(BaseModel):
    meal_type: str
    food_items: List[str]
    calories: int
    date: date

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    age: Optional[int] = None   # ← Agora é opcional
    gender: Optional[str] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    pass

class AuthUser(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    meals: List[MealResponse] = []

    class Config:
        orm_mode = True
