from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from fastapi import Depends, FastAPI
from typing_extensions import Annotated



class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password:str
    database_name:str
    database_username: str
    secret_key :str
    algorithm :str
    access_token_expire_minutes: int =90

    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()




   
    






