from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from database import get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

@router.post("/", summary="Cria um novo usuário")
def create_user(name: str, age: int, gender: str, db: Session = Depends(get_db)):
    new_user = User(name=name, age=age, gender=gender)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "data": new_user}


@router.get("/", summary="Lista todos os usuários")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"message": "Users retrieved successfully", "data": users}


@router.put("/{user_id}", summary="Atualiza um usuário pelo ID")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "data": user}


@router.delete("/{user_id}", summary="Remove um usuário pelo ID")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully", "user_id": user_id}
