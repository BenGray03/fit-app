from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user

from .. import schemas, crud

router = APIRouter(prefix="")

@router.get(
    "/home/",
    response_model=schemas.UserStats,
    summary="homepage for every user."
)
def home(user: schemas.User = Depends(get_current_user),
         db: Session = Depends(get_db)):
    current_bodyweight = crud.get_latest_bodyweight(db, user.id)
    current_protien, current_calories = crud.get_todays_nutrition(db, user.id)

    return schemas.UserStats(username=user.username, latest_bodyweight=current_bodyweight, today_protein=current_protien, today_calories=current_calories)

    



       



