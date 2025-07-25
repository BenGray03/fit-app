
from fastapi import HTTPException, status


bad_IP_format = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
    detail="Invalid IP Address Format"
    )

too_many_attempts = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Too many attempts in the last 15 minutes! Please try again later."
    )

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid login information"
    )

user_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists"
    )

username_taken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already registered"
    )