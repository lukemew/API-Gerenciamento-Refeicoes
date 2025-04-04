from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import get_db
from app.models.models import Base, engine
from app.routes import users, meals, reports, views, activities, auth
from database.token import verify_token

app = FastAPI()

# 🗂️ Criação automática das tabelas no startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# 📁 Diretórios de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Middleware para proteger rotas privadas
# 🌐 Middleware global de autenticação
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Rotas públicas que não requerem autenticação
    public_routes = {
        "/login", "/register"
    }

    print(f"Path acessado: {request.url.path}")
    
    # Verifica se a rota é pública
    if any(
        request.url.path == path or 
        request.url.path.startswith(path) 
        for path in public_routes
    ):
        return await call_next(request)
    
    # Verifica o token para rotas privadas
    token = request.cookies.get("access_token")
    print(f"Token encontrado: {bool(token)}")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        # Verifica o token (usando sua função existente)
        db = next(get_db())  # Obter uma sessão do banco de dados
        verify_token(access_token=token, db=db)  # ✅ Validação única
        return await call_next(request)
    except Exception as e:
        print(f"Erro na autenticação: {e}")
        return RedirectResponse(url="/login")
    
    @app.get('/favicon.ico', include_in_schema=False)
    async def favicon():
        return FileResponse("static/favicon.ico")

# 🔌 Registra os roteadores
app.include_router(auth.router, tags=["Auth"])
app.include_router(views.router, tags=["Views"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(activities.router, prefix="", tags=["Views"])

