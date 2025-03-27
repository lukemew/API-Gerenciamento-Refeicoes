from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import ActivityLog, User
from pydantic import BaseModel

from typing import List, Optional

router = APIRouter()

# Definição das calorias queimadas por atividade e intensidade
CALORIES_PER_MINUTE = {
    "Bike": {"baixa": 5, "média": 8, "alta": 15},
    "Caminhada": {"baixa": 3, "média": 5, "alta": 8},
    "Corrida": {"baixa": 6, "média": 10, "alta": 18},
    "Natação": {"baixa": 7, "média": 12, "alta": 20},
    "Musculação": {"baixa": 4, "média": 7, "alta": 12},
}

# Schemas Pydantic devem ser definidos ANTES de serem usados
class ActivityBase(BaseModel):
    activity: str
    intensity: str
    duration: int
    calories_burned: Optional[float] = None

class ActivityCreate(ActivityBase):
    user_id: int

class ActivityUpdate(BaseModel):
    activity: Optional[str] = None
    intensity: Optional[str] = None
    duration: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    user_id: int
    date: date

    class Config:
        from_attributes = True 
        arbitrary_types_allowed = True

# Agora sim podemos usar ActivityResponse nos decoradores
@router.post("/", response_model=ActivityResponse)
def log_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se o usuário existe
        user = db.query(User).filter(User.id == activity.user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
            )

        # Valida atividade e intensidade
        if activity.activity not in CALORIES_PER_MINUTE:
            raise HTTPException(
                status_code=400,
                detail=f"Atividade inválida. Opções válidas: {list(CALORIES_PER_MINUTE.keys())}"
            )
        
        if activity.intensity not in CALORIES_PER_MINUTE[activity.activity]:
            raise HTTPException(
                status_code=400,
                detail=f"Intensidade inválida para {activity.activity}. Opções: {list(CALORIES_PER_MINUTE[activity.activity].keys())}"
            )

        # Calcula calorias queimadas
        calories_burned = (
            CALORIES_PER_MINUTE[activity.activity][activity.intensity] *
            activity.duration
        )

        # Cria a atividade
        new_activity = ActivityLog(
            user_id=activity.user_id,
            activity=activity.activity,
            intensity=activity.intensity,
            duration=activity.duration,
            calories_burned=calories_burned
            # A data será preenchida automaticamente pelo default no modelo
        )

        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado: {str(e)}"
        )

@router.put("/{activity_id}", summary="Atualiza uma atividade")
def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    db: Session = Depends(get_db)
):
    try:
        activity = db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
        if not activity:
            raise HTTPException(
                status_code=404,
                detail="Atividade não encontrada"
            )

        # Atualiza apenas os campos fornecidos
        update_data = activity_data.dict(exclude_unset=True)
        
        if 'activity' in update_data or 'intensity' in update_data:
            # Se atividade ou intensidade mudaram, recalcula calorias
            new_activity = update_data.get('activity', activity.activity)
            new_intensity = update_data.get('intensity', activity.intensity)
            new_duration = update_data.get('duration', activity.duration)
            
            if new_activity not in CALORIES_PER_MINUTE:
                raise HTTPException(
                    status_code=400,
                    detail="Atividade inválida"
                )
            
            if new_intensity not in CALORIES_PER_MINUTE[new_activity]:
                raise HTTPException(
                    status_code=400,
                    detail="Intensidade inválida para esta atividade"
                )
            
            update_data['calories_burned'] = (
                CALORIES_PER_MINUTE[new_activity][new_intensity] *
                new_duration
            )

        for field, value in update_data.items():
            setattr(activity, field, value)

        db.commit()
        db.refresh(activity)
        return activity

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro no banco de dados: {str(e)}"
        )

@router.delete("/{activity_id}", summary="Remove uma atividade")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    try:
        activity = db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
        if not activity:
            raise HTTPException(
                status_code=404,
                detail="Atividade não encontrada"
            )

        db.delete(activity)
        db.commit()
        return {"message": "Atividade removida com sucesso"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro no banco de dados: {str(e)}"
        )

# Rota para a página HTML
@router.get("/", response_model=List[ActivityResponse])
def get_activities(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(ActivityLog)
        if user_id:
            query = query.filter(ActivityLog.user_id == user_id)
        return query.all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")