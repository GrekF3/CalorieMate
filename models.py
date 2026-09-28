from datetime import datetime
from sqlalchemy import Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    tdee: Mapped[int] = mapped_column(Integer, nullable=False)
    calories_goal: Mapped[int] = mapped_column(Integer, nullable=False)

    meals: Mapped[list["Meal"]] = relationship("Meal", back_populates="user", cascade="all, delete-orphan")


class FoodCache(Base):
    __tablename__ = "food_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    of_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    nutrients: Mapped[dict] = mapped_column(JSON, nullable=False)

    meals: Mapped[list["Meal"]] = relationship("Meal", back_populates="food", cascade="all, delete-orphan")


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    food_cache_id: Mapped[int] = mapped_column(ForeignKey("food_cache.id"), nullable=False, index=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    portion: Mapped[str] = mapped_column(String, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="meals")
    food: Mapped[FoodCache] = relationship("FoodCache", back_populates="meals")