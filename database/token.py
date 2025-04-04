from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status, Cookie
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
from database.database import get_db
from app.models.models import User as UserModel

# 🔐 Carregando variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# 🔑 Geração do token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token ausente")
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = db.query(UserModel).filter(UserModel.name == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

# 🚪 Logout: remove o cookie de autenticação
def logout(request: Request):
    response = RedirectResponse(url='/login')
    response.delete_cookie("access_token")
    return response
