from pydantic import BaseModel
from datetime import datetime
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
    current_bodyweight: float | None = None
    protein_goal: int | None = None
    calorie_goal: int | None = None

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

    class Config:
        from_attributes = True

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

class Token(BaseModel):
    access_token: str
    token_type: str

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

class Attempt:
    def __init__(self, ip):
        ip: ipaddress
        no_attempts = 1
        first_attempt =datetime.now()
    
    def is_blocked(self) -> bool:
        if self.no_attempts >= 10:
            return True
        else:
            return False
