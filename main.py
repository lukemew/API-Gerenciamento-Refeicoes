from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.meals import router as meals_router

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(meals_router, prefix="/meals", tags=["Meals"])

@app.get("/")
def root():
    return {"message": "API de Gerenciamento de Dieta com Banco de Dados SQLite"}
