from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./test.db"

# Configuração do SQLAlchemy Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configuração da sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
