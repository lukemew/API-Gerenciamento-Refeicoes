from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Define tamanho máximo
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)  # Define tamanho máximo
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meal_type = Column(String(50), nullable=False)  # Define tamanho máximo
    food_items = Column(String(255), nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    # Relacionamento com User
    user = relationship("User", back_populates="meals")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity = Column(String(50), nullable=False)
    intensity = Column(String(50))
    duration = Column(Integer)  
    calories_burned = Column(Float)  
    date = Column(Date, nullable=False, default=datetime.now().date())

    user = relationship("User")

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)
