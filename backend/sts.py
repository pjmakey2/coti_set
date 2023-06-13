import secrets, sys
import os

FP = os.path.realpath(os.path.curdir)
# You run main from the fastapi folder
sys.path.append(FP)
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exchange Crawler"
    VERSION: str = "/1"
    ENVIROMENT: str = "DEBUG"
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # URL DEFINES
    CC: str = "https://www.cambioschaco.com.py/en/perfil-de-moneda/"
    BCP: str = 'https://www.bcp.gov.py/webapps/web/cotizacion/monedas'
    HEADERS: dict = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Linux",
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',        
    }

    DB_NAME: str = "exchange.sqlite"
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{FP}/{DB_NAME}"

    class Config:
        case_sensitive = True


settings = Settings(_env_file=f"{FP}/settings.env", _env_file_encoding="utf-8")
