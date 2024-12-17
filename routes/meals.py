from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Meal
from database import get_db
from pydantic import BaseModel
from typing import List, Optional
import datetime
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()



class MealCreate(BaseModel):
    user_id: int
    meal_type: str
    food_items: List[str]
    calories: int
    date: datetime.date



class MealUpdate(BaseModel):
    meal_type: Optional[str] = None
    food_items: Optional[List[str]] = None
    calories: Optional[int] = None
    date: Optional[datetime.date] = None



@router.post("/", summary="Cria uma nova refeição")
def add_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    try:

        food_items_str = ",".join(meal_data.food_items)

        new_meal = Meal(
            user_id=meal_data.user_id,
            meal_type=meal_data.meal_type,
            food_items=food_items_str,
            calories=meal_data.calories,
            date=meal_data.date
        )
        db.add(new_meal)
        db.commit()
        db.refresh(new_meal)
        return {"message": "Meal added successfully", "data": new_meal}
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the database.")
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid input data")



@router.get("/{user_id}", summary="Lista refeições de um usuário")
def get_meals_by_user(user_id: int, db: Session = Depends(get_db)):
    meals = db.query(Meal).filter(Meal.user_id == user_id).all()
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for this user")
    return {"message": "Meals retrieved successfully", "data": meals}



@router.put("/{meal_id}", summary="Atualiza uma refeição pelo ID")
def update_meal(meal_id: int, meal_data: MealUpdate, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    try:
        
        for key, value in meal_data.dict(exclude_unset=True).items():
            if key == "food_items" and value is not None:
                value = ",".join(value)  
            setattr(meal, key, value)

        db.commit()
        db.refresh(meal)
        return {"message": "Meal updated successfully", "data": meal}

    except Exception as e:
        db.rollback()
        print(f"Update Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update meal")


@router.delete("/{meal_id}", summary="Remove uma refeição pelo ID")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    try:
        db.delete(meal)
        db.commit()
        return {"message": "Meal deleted successfully", "meal_id": meal_id}

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Delete Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete meal")
