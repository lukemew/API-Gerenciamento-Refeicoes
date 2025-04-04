from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from app.models.models import User as UserModel
from app.schemas.schemas import UserCreate, AuthUser


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_padrão_segura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: UserCreate):
        user_exists = self.db_session.query(UserModel).filter_by(name=user.name).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        
        hashed_password = crypt_context.hash(user.password)
        user_model = UserModel(
            name=user.name,
            age=user.age,
            gender=user.gender,
            password=hashed_password
        )

        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            return {"message": "User created successfully"}
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating user"
            )

    def user_login(self, user: AuthUser, expires_in: int = 30):
        from database.token import create_access_token  # Importação tardia
        user_on_db = self.db_session.query(UserModel).filter_by(name=user.username).first()

        if not user_on_db or not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_in)
        payload = {"sub": user.username, "exp": exp}

        access_token = create_access_token(payload, expires_delta=timedelta(minutes=expires_in))

        return {"access_token": access_token, "exp": exp.isoformat()}
