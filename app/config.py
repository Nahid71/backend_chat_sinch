from pydantic import BaseSettings
import os

class Settings(BaseSettings):

    # use_ngrok:str = os.getenv("USE_NGROK", "False") == "True"

    db_username : str = os.getenv('DB_USERNAME')
    db_pwd : str = os.getenv('DB_PWD')
    db_env : str = os.getenv('DB_ENV')

    secret_key: str = os.getenv('SECRET_KEY')
    secret_key_front : str = os.getenv('SECRET_KEY_FRONT')

    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: str = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    base_url :str = os.getenv('BASE_URL')

    openai_key: str = os.getenv('OPENAI_KEY')
    sinch_key: str = os.getenv('SINCH_APP_KEY')
    sinch_secret: str = os.getenv('SINCH_APP_SECRET')
    sinch_project_id: str = os.getenv('SINCH_PROJECT_ID')

    class Config:
        env_file = ".env"


settings = Settings()