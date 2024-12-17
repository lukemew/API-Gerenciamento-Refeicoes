from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import User
from database import get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    age: int
    gender: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


@router.post("/", summary="Cria um novo usuário")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(name=user.name, age=user.age, gender=user.gender)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "data": new_user}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/", summary="Lista todos os usuários")
def list_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return {"message": "Users retrieved successfully", "data": users}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/{user_id}", summary="Atualiza um usuário pelo ID")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return {"message": "User updated successfully", "data": user}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{user_id}", summary="Remove um usuário pelo ID")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully", "user_id": user_id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
