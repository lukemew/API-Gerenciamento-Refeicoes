from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine

# Modelo de Usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    # Relacionamento com a tabela Meal
    meals = relationship("Meal", back_populates="user")

# Modelo de Refeição
class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(String, nullable=False)
    food_items = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    # Relacionamento com a tabela User
    user = relationship("User", back_populates="meals")

Base.metadata.create_all(bind=engine)