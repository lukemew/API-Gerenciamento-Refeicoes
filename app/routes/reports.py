from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import Meal, User, ActivityLog
from database.database import get_db
from sqlalchemy.sql import func
from database.token import verify_token

router = APIRouter()  # 🔒 Todas as rotas exigem token


@router.get("/user/{user_id}/calories", summary="Resumo de calorias por usuário")
def get_user_calories(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        total_calories_consumed = db.query(func.coalesce(func.sum(Meal.calories), 0)).filter(Meal.user_id == user_id).scalar()
        total_calories_burned = db.query(func.coalesce(func.sum(ActivityLog.calories_burned), 0)).filter(ActivityLog.user_id == user_id).scalar()

        # 🛠 Convertendo para float para evitar erro de tipo
        total_calories_consumed = float(total_calories_consumed)
        total_calories_burned = float(total_calories_burned)

        balance = total_calories_consumed - total_calories_burned

        return {
            "user_id": user_id,
            "name": user.name,
            "total_calories_consumed": total_calories_consumed,
            "total_calories_burned": total_calories_burned,
            "balance": balance,
            "message": f"{user.name} consumiu {total_calories_consumed} calorias e gastou {total_calories_burned} calorias. Balanço final: {balance} calorias."
        }

    except SQLAlchemyError as e:
        print(f"Erro no banco de dados: {str(e)}")  # Log do erro real
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
