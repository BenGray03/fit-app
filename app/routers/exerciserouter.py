from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user

from .. import models, crud, schemas, exceptions

exerciseRouter = APIRouter(prefix="/exercises", tags=["exercise"])

@exerciseRouter.get(
    "/exercises",
    response_model=list[models.Exercise],
    summary="Get a list of the users exercises"
)
def get_exercises(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_users_exercises(db, current_user.id)

@exerciseRouter.post(
    "/add",
    summary="add exercises"
)
def add_exercises(exercise = schemas.CreateExercise, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_exercise(db, current_user.id, exercise)

@exerciseRouter.patch(
    "/edit/{exercise_id}",
    summary="edit exercies"
)
def edit_exercises(updated: schemas.ExerciseUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated = crud.update_exercise(db, current_user.id, updated)
    if not updated:
        raise exceptions.not_updated
    return updated

@exerciseRouter.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete exercises"
)
def delete_exercise(exercise_id:int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.delete_exercise(db, exercise_id)