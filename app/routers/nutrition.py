from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user

from .. import crud, models, schemas, exceptions

nutritionRouter = APIRouter(prefix="/nutrition")

@nutritionRouter.get(
    "/today/",
    response_model=schemas.DailyNutritionOut,
    summary="Get todays goals and goal progress"
)
def get_todays_nutrition(date: date, db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    todays_goals = crud.get_specific_nutrition(db, current_user.id, date)
    return crud.to_schema(todays_goals, schemas.DailyNutritionOut)

@nutritionRouter.get(
    "/history",
    summary="get previous days goal progress"
)
def get_prev_days(start_date: date, days: int = Query(7, ge=1, le=365),db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    cuttoff_date = start_date - days
    return crud.get_range_nutrition(db, current_user.id, start_date, cuttoff_date)


@nutritionRouter.patch(
    "/goals/",
    response_model=schemas.DailyNutritionOut
)
def update_nutrition(payload: schemas.NutritionGoalsPatch, db: Session = Depends(get_db), current_user:models.User = Depends(get_current_user)):
    if payload.calorie_goal is None and payload.protein_goal is None and payload.calories is None and payload.protein is None:
        raise exceptions.no_goals_in_payload

    updated_nutrition : models.DailyNutrition = crud.update_nutrition_entry(db=db, user_id=current_user.id, day=payload.date_patch, calories=payload.calories, calorie_goal=payload.calorie_goal, protein=payload.protein, protein_goal=payload.protein_goal)
    return crud.to_schema(updated_nutrition, schemas.DailyNutritionOut)
    
    
    
