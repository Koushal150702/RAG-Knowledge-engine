""" This is basically the skeleton of the env variables with default values """
""" The .env file will hold the actual values for these constants like passwords"""
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    """
    This class is the 'Contract' for our application. 
    It defines everything the app NEEDS to know.
    """

# App component
    APP_NAME: str = 'AI knowledge engine'

# Database component

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASS: str = 'password'
    DB_NAME: str = 'knowledge_db'

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def DATABASE_URL(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

settings = Settings()
