from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Game Connect"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
