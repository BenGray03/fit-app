from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user

from .. import models

exerciseRouter = APIRouter(prefix="/exercises", tags=["exercise"])

@exerciseRouter.get(
    "/exercises",
    summary="Get a list of the users exercises"
)
def get_exercises(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pass

@exerciseRouter.post(
    "/add",
    summary="add exercises"
)
def add_exercises(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pass

@exerciseRouter.patch(
    "/edit",
    summary="edit exercies"
)
def edit_exercises(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pass

@exerciseRouter.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete exercises"
)
def delete_exercise(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    pass