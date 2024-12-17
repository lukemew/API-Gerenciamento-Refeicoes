from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Meal, User
from database import get_db
from sqlalchemy.sql import func

router = APIRouter()


@router.get("/user/{user_id}/calories", summary="Resumo de calorias por usuário")
def get_user_calories(user_id: int, db: Session = Depends(get_db)):
    try:
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
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
