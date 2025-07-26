from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from app import crud, schemas, utils
from ..database import get_db
from ipaddress import ip_address
from .. import exceptions



#Authentication Router - any login or signup or anything that may need some technical anaylsis...
authRouter = APIRouter(prefix="/auth", tags=["auth"]) 

#Might have to make sure that it is secure to sql injection
@authRouter.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Login as user, returns a JWT Token"
)
def login(login_data: OAuth2PasswordRequestForm = Depends(), request :Request = None, db:Session = Depends(get_db)):
    try:
        ip = ip_address(request.client.host)
    except ValueError:
        raise exceptions.bad_IP_format
    
    if utils.check_ip_blocked(ip):
        raise exceptions.too_many_attempts
    
    user = crud.authenticate_user(db=db, username=login_data.username, password=login_data.password)

    if not user:
        utils.add_attempt(ip)
        raise exceptions.invalid_credentials
    #successful user login
    access_token = utils.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
    
@authRouter.post(
    "/signup/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user."
)
def signup(user: schemas.UserCreate, db:Session = Depends(get_db)):
    existing = crud.get_user_from_username(db=db, username=user.username)
    if existing:
        raise exceptions.user_exists
    try:
        db_user = crud.create_user(db, user)
    except IntegrityError:
        raise exceptions.username_taken
    
    return db_user

