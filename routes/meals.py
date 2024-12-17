from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Meal
from database import get_db
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()


class MealUpdate(BaseModel):
    meal_type: Optional[str] = None
    food_items: Optional[List[str]] = None
    calories: Optional[int] = None
    date: Optional[datetime.date] = None


@router.post("/meals", summary="Cria uma nova refeição")
def add_meal(user_id: int, meal_type: str, food_items: List[str], calories: int, date: datetime.date, db: Session = Depends(get_db)):
    new_meal = Meal(user_id=user_id, meal_type=meal_type, food_items=food_items, calories=calories, date=date)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return {"message": "Meal added successfully", "data": new_meal}


@router.get("/meals/{user_id}", summary="Lista refeições de um usuário")
def get_meals_by_user(user_id: int, db: Session = Depends(get_db)):
    meals = db.query(Meal).filter(Meal.user_id == user_id).all()
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for this user")
    return {"message": "Meals retrieved successfully", "data": meals}


@router.put("/meals/{meal_id}", summary="Atualiza uma refeição pelo ID")
def update_meal(meal_id: int, meal_data: MealUpdate, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    for key, value in meal_data.dict(exclude_unset=True).items():
        setattr(meal, key, value)
    db.commit()
    db.refresh(meal)
    return {"message": "Meal updated successfully", "data": meal}


@router.delete("/meals/{meal_id}", summary="Remove uma refeição pelo ID")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    db.delete(meal)
    db.commit()
    return {"message": "Meal deleted successfully", "meal_id": meal_id}
