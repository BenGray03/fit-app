from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from app import crud, schemas, utils
from ..database import get_db
from ipaddress import ip_address



authRouter = APIRouter(prefix="/auth", tags=["auth"]) 

#Might have to make sure that it is secure to sql injection
@authRouter.post(
    "/login/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
    summary="Login as user"
)
def login(username: str, password: str, ip_as_str: str, db:Session = Depends(get_db)):

    try:
        ip = ip_address(ip_as_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid IP Address Format")
    
    if utils.check_ip_blocked(ip):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Too many attempts in the last 15 minutes! Please try again later."
        )
    user = crud.authenticate_user(db=db, username=username, password=password)
    if user:
        user_out = schemas.UserOut(username=user.username, id=user.id)
        return user_out
    else:
        utils.add_attempt(ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invlaid login information"
        )
    
@authRouter.post(
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

@authRouter.post(
    "/token/",
    status_code=status.HTTP_200_OK,
    summary="Get JWT token"
)
def obtain_token(form: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = crud.authenticate_user(db=db, username=form.username, password=form.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect login details.",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token = utils.create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}