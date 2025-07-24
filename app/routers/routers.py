from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="")


@router.post(
    "/signup/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user."
)
def signup(user: schemas.UserCreate, db:Session = Depends(get_db)):
    existing = crud.get_user_from_username(db=db, username=user.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    try:
        db_user = crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    return db_user




       



