from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from ..utils import get_current_user
from .. import crud, schemas, models

bodyweightRouter = APIRouter("/weight", tags=["weight"])

@bodyweightRouter.get(
    "/today",
    summary="get most recent bodyweight information."
)
def bodyweight_today(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_latest_bodyweight(db, current_user.id)


@bodyweightRouter.get(
    "/history",
    summary="get a list of bodyweight entries"
)
def get_bodyweight_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_bodyweight_history(db, current_user.id)

@bodyweightRouter.delete(
    "/{bodyweight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="delete bodyweight entry"
)
def delete_bodyweight(bodyweight_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    crud.delete_bodyweight(db, bodyweight_id, current_user.id)

@bodyweightRouter.post(
    "/add",
    summary="add bodyweight entry"
)
def add_bodyweight():
    pass