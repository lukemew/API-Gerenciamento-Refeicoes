from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Meal, User
from database import get_db
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

@router.get("/user/{user_id}/calories", summary="Resumo de calorias por usuário")
def get_user_calories(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    meals = db.query(Meal).filter(Meal.user_id == user_id).all()
    total_calories = sum(meal.calories for meal in meals)

    return {
        "user_id": user_id,
        "name": user.name,
        "total_calories": total_calories,
        "message": f"{user.name} consumed a total of {total_calories} calories."
    }


@router.get("/meals/top", summary="Refeições mais calóricas")
def get_top_caloric_meals(limit: int = 5, db: Session = Depends(get_db)):
    meals = db.query(Meal).order_by(Meal.calories.desc()).limit(limit).all()
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found")

    return {
        "message": "Top caloric meals retrieved successfully",
        "data": [
            {"meal_id": meal.id, "meal_type": meal.meal_type, "calories": meal.calories}
            for meal in meals
        ]
    }


@router.get("/users/top", summary="Usuários com maior consumo calórico")
def get_top_users(limit: int = 5, db: Session = Depends(get_db)):
   
    from sqlalchemy.sql import func
    users_calories = (
        db.query(User.name, func.sum(Meal.calories).label("total_calories"))
        .join(Meal, User.id == Meal.user_id)
        .group_by(User.id, User.name)
        .order_by(func.sum(Meal.calories).desc())
        .limit(limit)
        .all()
    )

    if not users_calories:
        raise HTTPException(status_code=404, detail="No data found")

    return {
        "message": "Top users by calorie consumption",
        "data": [
            {"user_name": name, "total_calories": total_calories}
            for name, total_calories in users_calories
        ]
    }
