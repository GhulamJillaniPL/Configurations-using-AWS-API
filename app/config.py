from pydantic import BaseSettings

class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    api_secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()

