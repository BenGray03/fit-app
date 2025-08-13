from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, get_db
from .routers.routers import router
from .routers.authrouter import authRouter
from .routers.nutrition import nutritionRouter
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
app.include_router(authRouter)
app.include_router(router)
app.include_router(nutritionRouter)

@app.post("/input/", response_model=schemas.UserInputCreate)
def create_input(user_input: schemas.UserInputCreate, db: Session = Depends(get_db)):
    db_input = crud.create_user_input(db, user_input)
    return db_input


