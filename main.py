from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, meals, reports, views, activities
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from fastapi.staticfiles import StaticFiles
from models import Base, engine

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
import models

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(views.router, tags=["Views"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(activities.router, prefix="", tags=["Views"])  # Para a página HTML

