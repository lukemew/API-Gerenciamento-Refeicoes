from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, meals, reports 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/", summary="Rota inicial")
def root():
    return {"message": "API de Gerenciamento de Dieta com SQLite"}
