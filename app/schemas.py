from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
import ipaddress

class UserInputCreate(BaseModel):
    username: str
    input_text: str

class UserInput(BaseModel):
    id: int
    username: str
    input_text: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    name:str


class User(BaseModel):
    id: int
    username: str
    current_bodyweight: float | None = None
    protein_goal: int | None = None
    calorie_goal: int | None = None

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id:int
    username:str
    name:str
    class Config:
        from_attributes = True

class UserStats(BaseModel):
    username: str
    latest_bodyweight: float | None
    today_calories: int
    today_protein: int

class Token(BaseModel):
    access_token: str
    token_type: str



class CreateExercise(BaseModel):
    id: int
    user_id: int
    name: str
    sets: int
    reps: int
    pb: float | None = None
    weight: float | None = None

class Exercise(BaseModel):
    id: int
    user_id: int
    name: str
    sets: int
    reps: int
    pb: float | None = None
    weight: float | None = None

    class Config:
        from_attributes = True


class BodyweightBase(BaseModel):
    weight: float

class BodyweightCreate(BodyweightBase):
    pass 

class Bodyweight(BodyweightBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True


class NutritionGoalsPatch(BaseModel):
    date_patch: date = Field(None, description="Defaults to today's date (UTC).")
    calories: Optional[int] = Field(None, ge=0, le=20000)
    calorie_goal: Optional[int] = Field(None, ge=0, le=20000)
    protein: Optional[int] = Field(None, ge=0, le=1000)
    protein_goal: Optional[int] = Field(None, ge=0, le=1000)

class DailyNutritionOut(BaseModel):
    id:int
    user_id: int
    date_out: date
    calories:int
    protien: int
    calorie_goal: int
    protein_goal:int

    class Config:
        from_attributes = True

class Attempt:
    def __init__(self, ip: str):
        self.ip: ipaddress.IPv4Address = ipaddress.ip_address(ip)
        self.no_attempts: int = 1
        self.first_attempt: datetime = datetime.now()

    def is_blocked(self) -> bool:
        return self.no_attempts >= 10

