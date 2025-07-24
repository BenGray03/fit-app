from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from .database import Base
from datetime import datetime

class UserInput(Base):
    __tablename__ = "user_inputs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    input_text = Column(String)
    created_at = Column(DateTime, default=datetime.now)

#User table has ID, USERNAME, HASHED_PASSWORD, CURRENT_BODYWEIGHT, PROTEIN_GOAL and CALORIE_GOAL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    current_bodyweight = Column(Float, nullable=True)
    protein_goal = Column(Integer, nullable=True)
    calorie_goal = Column(Integer, nullable=True)

class BodyweightHistory(Base):
    __tablename__ = "bodyweight_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=True)
    date = Column(DateTime, default=datetime.now)

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    pb = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)

class DailyNutrition(Base):
    __tablename__ = "daily_nutrition"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.now)
    calories = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)