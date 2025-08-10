from datetime import date, datetime, time, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
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
        name=user.name
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

def get_specific_nutrition(db: Session, user_id: int, date: datetime):
    start = datetime(date.year, date.month, date.day)
    end = start + timedelta(days=1)

    entry: models.DailyNutrition = db.query(models.DailyNutrition)\
            .filter(and_(models.DailyNutrition.user_id == user_id,
                         models.DailyNutrition.date >= start,
                         models.DailyNutrition.date <= end))\
            .order_by(models.DailyNutrition.date.desc())\
            .first()
    return {
        "Protein_Progress": entry.protein if entry else 0,
        "Protein_Goal": entry.protein_goal if entry else 0,
        "Calorie_Progress": entry.calories if entry else 0,
        "Calorie_Goal": entry.calorie_goal if entry else 0
    }

def get_range_nutrition(db: Session, user_id: int, start: datetime, end: datetime) :

    entries = (db.query(models.DailyNutrition)\
            .filter(and_(models.DailyNutrition.user_id == user_id,
                        models.DailyNutrition.date >= start,
                        models.DailyNutrition.date <= end,))\
            .order_by(models.DailyNutrition.date.asc())\
            .all())
    return entries


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

