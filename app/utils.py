from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
import openai
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from .config import settings
from jwt import PyJWTError, encode
from .schemas import Attempt
from . import crud, exceptions

login_attempts = []

openai.api_key = settings.OPEN_AI_KEY

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_chatgpt_response(user_prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful fitness assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise exceptions.invalid_credentials
    except PyJWTError:
        raise exceptions.invalid_credentials
    
    user = crud.get_user_from_id(db, user_id)
    
    if user is None:
        raise exceptions.invalid_credentials

    return user

def create_access_token(data: dict) -> str:
    to_encode = dict.copy(data)
    time_at_now = datetime.now()
    expiry = int((time_at_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    to_encode.update({"exp" : expiry, "issued": int(time_at_now.timestamp())})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
    
def check_ip_blocked(ip)->bool:
    update_attempts()
    attempt = get_attempt(ip)
    if attempt is None:
        return False
    else: 
        return attempt.is_blocked()
    
def add_attempt(ip):
    update_attempts()
    attempt = get_attempt(ip)
    if attempt is None:
        new_attempt = Attempt(ip)
        login_attempts.append(new_attempt)
    else:
        attempt.ip += 1
        
def get_attempt(ip)-> Attempt:
    for attempt in login_attempts:
        if attempt.ip == ip:
            return attempt
    return None

def update_attempts():
    to_remove = []
    for attempt in login_attempts:
        print(attempt)
        if datetime.now() - attempt.first_attempt < timedelta(minutes=15):
            to_remove.append(attempt)
    
    for removed in to_remove:
        login_attempts.remove(removed)