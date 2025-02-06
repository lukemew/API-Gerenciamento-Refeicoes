from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", summary="Página inicial")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/users", summary="Lista de usuários")
def list_users_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user.html", {"request": request, "users": users})

@router.post("/add-user", summary="Adiciona um novo usuário")
def add_user(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db)
):
    new_user = User(name=name, age=age, gender=gender)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)
