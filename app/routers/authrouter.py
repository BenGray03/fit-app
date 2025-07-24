from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from app import crud, schemas, utils
from ..database import get_db
from ipaddress import ip_address


#Authentication Router - any login or signup or anything that may need some technical anaylsis
authRouter = APIRouter(prefix="/auth", tags=["auth"]) 

#Might have to make sure that it is secure to sql injection
@authRouter.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Login as user, returns a JWT Token"
)
def login(login_data: OAuth2PasswordRequestForm = Depends(), ip_as_str: str="", db:Session = Depends(get_db)):
    try:
        ip = ip_address(ip_as_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid IP Address Format")
    
    if utils.check_ip_blocked(ip):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Too many attempts in the last 15 minutes! Please try again later."
        )
    user = crud.authenticate_user(db=db, username=login_data.username, password=login_data.password)
    if not user:
        utils.add_attempt(ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invlaid login information"
        )
    #successful user login
    access_token = utils.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
    
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

