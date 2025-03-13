from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)  # Confirme que esta linha existe
    gender = Column(String, nullable=False)
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meal_type = Column(String, nullable=False)
    food_items = Column(String, nullable=False)  # Lista armazenada como string separada por vírgula
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    # Relacionamento com User
    user = relationship("User", back_populates="meals")



Base.metadata.create_all(bind=engine)