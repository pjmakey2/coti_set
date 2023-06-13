import secrets, sys
import os
FP = os.path.realpath(os.path.curdir)
#You run main from the fastapi folder
sys.path.append(FP)
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Exchange Crawler'
    VERSION: str = '/1'
    ENVIROMENT: str = 'DEBUG'
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    #URL DEFINES
    HIST_CC: str = 'https://www.cambioschaco.com.py/en/perfil-de-moneda/?currency=usd'
    DB_NAME: str = 'exchange.sqlite'
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{FP}/{DB_NAME}'

    class Config:
        case_sensitive = True

settings = Settings(_env_file=f'{FP}/settings.env', 
                    _env_file_encoding='utf-8')
