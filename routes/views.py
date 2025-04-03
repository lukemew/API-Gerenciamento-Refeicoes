from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Meal
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", summary="Página inicial")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/users", summary="Lista de usuários")
def list_users_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user.html", {"request": request, "users": users})

@router.get("/activities", summary="Página de atividades")
def activities_page(request: Request):
    return templates.TemplateResponse("activities.html", {"request": request})

@router.get("/meals", summary="Página de gerenciamento de refeições")
def list_meals_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("meals.html", {"request": request})

@router.get("/api/users", summary="Lista todos os usuários")
def list_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return {"message": "Users retrieved successfully", "data": users}
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar usuários")

@router.get("/api/meals/")
def get_meals(user_id: int, db: Session = Depends(get_db)):
    meals = db.query(Meal).filter(Meal.user_id == user_id).all()
    return meals

@router.get("/api/meals/{meal_id}", summary="Obtém uma refeição específica")
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return meal


@router.post("/add-user", summary="Adiciona um novo usuário")
def add_user(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        new_user = User(name=name, age=age, gender=gender)
        db.add(new_user)
        db.commit()
        return RedirectResponse(url="/users", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao adicionar usuário")


from models import Meal  # Certifique-se de importar o modelo Meal

@router.get("/reports", summary="Página de relatórios")
def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})


@router.post("/add-meal", summary="Adiciona uma nova refeição")
def add_meal(
    request: Request,
    user_id: int = Form(...),
    meal_type: str = Form(...),
    food_items: str = Form(...),
    calories: int = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Converte a string de food_items para uma lista
        food_items_list = food_items.split(',')

        new_meal = Meal(
            user_id=user_id,
            meal_type=meal_type,
            food_items=",".join(food_items_list),  # Salva como string no banco
            calories=calories,
            date=date
        )
        db.add(new_meal)
        db.commit()
        return RedirectResponse(url="/meals", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar refeição: {e}")
        raise HTTPException(status_code=500, detail="Erro ao adicionar refeição")
