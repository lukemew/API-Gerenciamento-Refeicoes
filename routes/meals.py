from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from models import Meal, User
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

@router.get("/", summary="Lista refeições por usuário")
def get_meals(
    user_id: int = Query(..., description="ID do usuário"),
    db: Session = Depends(get_db)
):
    # Força uma nova consulta sem cache
    meals = db.query(Meal).filter(Meal.user_id == user_id).execution_options(expire_on_commit=True).all()
    return meals

@router.post("/", summary="Cria uma nova refeição")
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se o usuário existe - igual ao activities
        user = db.query(User).filter(User.id == meal_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Converte food_items para string
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
        return new_meal  # Retorna o objeto direto igual ao activities
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro no banco de dados: {str(e)}"
        )


@router.put("/{meal_id}", summary="Atualiza uma refeição")
def update_meal(
    meal_id: int,
    meal_data: MealUpdate,
    db: Session = Depends(get_db)
):
    try:
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Refeição não encontrada")

        update_data = meal_data.dict(exclude_unset=True)
        
        if 'food_items' in update_data:
            update_data['food_items'] = ",".join(update_data['food_items'])
            
        for field, value in update_data.items():
            setattr(meal, field, value)

        db.commit()
        db.refresh(meal)
        return meal

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/{meal_id}", summary="Remove uma refeição")
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db)
):
    try:
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Refeição não encontrada")

        db.delete(meal)
        db.commit()
        return {"message": "Refeição removida com sucesso"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")