from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user

from .. import schemas

router = APIRouter(prefix="")

@router.get(
    "/home/",
    response_model=schemas.User,
    summary="homepage for every user."
)
def home(user: schemas.UserOut = Depends(get_current_user),
         db: Session = Depends(get_db)):
    pass



       



