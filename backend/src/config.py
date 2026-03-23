from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os 

load_dotenv() #important 

class Settings(BaseSettings):
    MODEL_NAME: str
    OLLAMA_HOST: str
    DB_PATH: str= str(Path(__file__).parent.parent / "data" / "hub.db")
    DATA_ROOT: Path = Path(__file__).parent.parent / "data"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()