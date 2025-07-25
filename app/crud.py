from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash_password, verify_password

#USER ACTIONS
def create_user_input(db: Session, user_input: schemas.UserInputCreate):
    db_input = models.UserInput(**user_input.model_dump())
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

def create_user(db: Session, user = schemas.UserCreate):
    hashed = hash_password(user.password)
    db_input = models.User(
        username=user.username,
        hashed_password = hashed, 
        current_bodyweight = user.current_bodyweight,
        protein_goal = user.protein_goal,
        calorie_goal = user.calorie_goal
        )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input
def authenticate_user(db :Session, username: str, password: str):
    user = get_user_from_username(db, username)

    if user is not None:
        if verify_password(password, user.hashed_password):
            return user
        else:
            return None
    else:
        return None

def get_user_from_id(db:Session, id:int):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user

def get_user_from_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

#
def create_exercise(db: Session, exercise = schemas.CreateExercise):
    db_input = models.Exercise(**exercise.model_dump())
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

def get_bodyweight_history(db: Session, user_id: int, skip: int = 0, limit:int = 100):
    return(
        db.query(models.BodyweightHistory)
           .filter(models.BodyweightHistory.id == user_id)
           .order_by(models.BodyweightHistory.date.desc())
           .offset(skip)
           .limit(limit)
           .all()
           )

def get_latest_bodyweight(db: Session, user_id: int):
    entry: models.BodyweightHistory = db.query(models.BodyweightHistory)\
           .filter(models.BodyweightHistory.user_id == user_id)\
           .order_by(models.BodyweightHistory.date.desc())\
           .first()
    return entry.weight if entry else 0

#doesnt get todays nutrition just the latest
def get_todays_nutrition(db: Session, user_id: int):
    entry: models.DailyNutrition = db.query(models.DailyNutrition)\
            .filter(models.DailyNutrition.user_id == user_id)\
            .order_by(models.DailyNutrition.date.desc())\
            .first()
    return (entry.protein, entry.calories) if entry else (0, 0)


def get_bodyweight(db: Session, bodyweight_ID: int):
    return (
        db.query(models.BodyweightHistory).get(bodyweight_ID)
        )

def update_bodyweight(db: Session, entry_id: int, updated: schemas.BodyweightCreate):
    entry = get_bodyweight(entry_id)
    if not entry:
        return None
    entry.weight = updated.weight
    entry.date = datetime.now()
    db.commit()
    db.refresh(entry)

def delete_bodyweight(db: Session, entry_id: int):
    entry = db.query(models.BodyweightHistory).get(entry_id)
    if not entry:
        return None
    db.delete(entry)
    db.commit()
    return entry

