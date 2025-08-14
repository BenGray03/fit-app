from datetime import date, datetime, time, timedelta
from typing import Optional
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



# Exercise Functions
def create_exercise(db: Session, user_id: int, exercise: schemas.CreateExercise):
    exercise_data = exercise.model_dump()
    entry = models.Exercise(user_id=user_id, **exercise_data)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_exercise(db: Session, exercise_id: int) -> models.Exercise:
    entry = db.query(models.Exercise).get(exercise_id)
    if not entry:
        return None
    else:
        return entry

def update_exercise(db: Session, exercise_id: int, updated: schemas.CreateExercise):
    exercise_entry: models.Exercise = get_exercise(db, exercise_id)
    updated_data = updated.model_dump(exclude_unset=True,exclude_none=True)
    for key in {"name","sets", "reps", "pb", "weight"} & updated_data.keys():
        setattr(exercise_entry, key, updated_data[key])

    db.commit()
    db.refresh(exercise_entry)
    return exercise_entry

def delete_exercise(db: Session, exercise_id: int):
    entry = db.query(models.Exercise).get(exercise_id)
    if not entry:
        return None
    db.delete(entry)
    db.commit()
    return entry

def get_users_exercises(db: Session, user_id: int)-> list[models.Exercise]:
    return db.query(models.Exercise)\
        .filter(models.Exercise.user_id == user_id)\
        .order_by(models.Exercise.name.asc())\
        .all()


#Bodyweight functions
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




#Nutrition functions
def get_specific_nutrition(db: Session, user_id: int, date: date)-> models.DailyNutrition:

    entry: models.DailyNutrition = db.query(models.DailyNutrition)\
            .filter(and_(models.DailyNutrition.user_id == user_id,
                         models.DailyNutrition.date == date))\
            .order_by(models.DailyNutrition.date.desc())\
            .first()
    
    if entry is None:
        #get last goals
        calorie_goal, protein_goal = get_prev_goals(db=db, user_id=user_id, date=date)
        #create new entry
        return init_nutrition_day(db=db, user_id=user_id, day=date, calories=0, calorie_goal=calorie_goal, protein=0, protein_goal=protein_goal)
    else:
        return entry


def get_range_nutrition(db: Session, user_id: int, start: date, end: date) :

    entries = (db.query(models.DailyNutrition)\
            .filter(and_(models.DailyNutrition.user_id == user_id,
                        models.DailyNutrition.date <= start,
                        models.DailyNutrition.date >= end))\
            .order_by(models.DailyNutrition.date.asc())\
            .all())
    return entries

def get_prev_goals(db: Session, user_id: int, date: date):
    entry: models.DailyNutrition = db.query(models.DailyNutrition)\
            .filter(and_(models.DailyNutrition.user_id == user_id,
                         models.DailyNutrition.date <= date))\
            .order_by(models.DailyNutrition.date.desc())\
            .first()
    if entry: 
        return entry.calorie_goal, entry.protein_goal
    else: 
        return 0,0

def init_nutrition_day(db: Session, user_id:int, day: date, calories: int,calorie_goal: int,protein:int, protein_goal:int) -> models.DailyNutrition:
    entry = models.DailyNutrition(
            user_id=user_id,
            date=day,
            calories=calories or 0,
            protein=protein or 0,
            calorie_goal=calorie_goal or 0,
            protein_goal=protein_goal or 0,
        )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry



def update_nutrition_entry(db: Session, user_id:int, day: date, calories:int, calorie_goal: int,protein: int, protein_goal:int)-> models.DailyNutrition:
    entry: Optional[models.DailyNutrition] = (
        db.query(models.DailyNutrition)
          .filter(
              and_(
                  models.DailyNutrition.user_id == user_id,
                  models.DailyNutrition.date == day,
              )
          )
          .one_or_none()
    )

    if entry is None:
        entry = init_nutrition_day(db=db, day=day,calories=calories, calorie_goal=calorie_goal, protein=protein,protein_goal=protein_goal)
        return entry
    else:
        if calorie_goal is not None:
            entry.calorie_goal = calorie_goal
        if protein_goal is not None:
            entry.protein_goal = protein_goal
        if protein is not None:
            entry.protein = protein
        if calories is not None:
            entry.calories = calories

    db.commit()
    db.refresh(entry)
    return entry

def to_schema(model_obj, schema_cls):
    return schema_cls.model_validate(model_obj, from_attributes=True)
