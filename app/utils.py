from datetime import timedelta, datetime
import openai
from passlib.context import CryptContext
from .config import settings
from jwt import encode
from .schemas import Attempt

login_attempts = []

openai.api_key = settings.OPEN_AI_KEY

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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

def create_access_token(data: dict) -> str:
    to_encode = dict.copy()
    time_at_now = datetime.now()
    expiry = time_at_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expiry, "issued": time_at_now})
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
        if timedelta.now() - attempt.first_attempt < timedelta(minutes=15):
            to_remove.append(attempt)
    
    for removed in to_remove:
        login_attempts.remove(removed)