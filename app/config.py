from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str

    ALGORITHM: str 

    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    OPEN_AI_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()