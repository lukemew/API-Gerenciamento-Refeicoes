from typing import List
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import datetime

app = FastAPI()

users = []
meals = []

class Meal(BaseModel):
    user_id: int
    meal_type: str  
    food_items: List[str]
    calories: int
    date: datetime.date

def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

@app.get("/")
async def root():
    return {"message": "Bem vindo à aplicação FastAPI!!"}

@app.get("/users")
async def list_users():
    return {
        "status": "success",
        "message": "Users retrieved successfully.",
        "data": users
    }

@app.post("/users")
async def create_user(name: str = Form(...), age: int = Form(...), gender: str = Form(...)):
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "age": age,
        "gender": gender
    }
    users.append(new_user)
    return {
        "status": "success",
        "message": "User registered successfully.",
        "data": new_user
    }

@app.post("/meals")
async def add_meal(meal: Meal):

    user = get_user_by_id(meal.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    meal_record = meal.dict()
    meal_record["id"] = len(meals) + 1
    meals.append(meal_record)
    
    return {
        "status": "success",
        "message": "Meal added successfully.",
        "data": meal_record
    }

@app.get("/meals/{user_id}")
async def get_meals_by_user(user_id: int):
    user_meals = [meal for meal in meals if meal["user_id"] == user_id]
    if not user_meals:
        raise HTTPException(status_code=404, detail="No meals found for this user.")
    
    return {
        "status": "success",
        "message": "Meals retrieved successfully.",
        "data": user_meals
    }

@app.put("/meals/{meal_id}")
async def update_meal(meal_id: int, meal: Meal):
    for m in meals:
        if m["id"] == meal_id:
            m.update(meal.dict())
            return {
                "status": "success",
                "message": "Meal updated successfully.",
                "data": m
            }
    raise HTTPException(status_code=404, detail="Meal not found.")

@app.delete("/meals/{meal_id}")
async def delete_meal(meal_id: int):
    for m in meals:
        if m["id"] == meal_id:
            meals.remove(m)
            return {
                "status": "success",
                "message": "Meal deleted successfully.",
                "data": m
            }
    raise HTTPException(status_code=404, detail="Meal not found.")
