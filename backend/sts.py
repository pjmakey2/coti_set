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
    MAX_HEADERS: dict = {
        "accept": "*/*",
        "accept-language": "en-US,en-PY;q=0.9,en;q=0.8,es-PY;q=0.7,es;q=0.6,en-GB;q=0.5",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-october-request-handler": "onHistoricoPartial",
        "x-october-request-partials": "",
        "x-requested-with": "XMLHttpRequest",
    }    
    CC: str = "https://www.cambioschaco.com.py/en/perfil-de-moneda/"
    SET: str = "https://www.set.gov.py/web/portal-institucional/cotizaciones"
    BCP: str = "https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante/anual"
    FAMILIAR: str = "https://www.familiar.com.py/p-servicios-cambios"
    MAXI: str = "https://www.maxicambios.com.py/"
    EXPANSION: str = "https://datosmacro.expansion.com/divisas/paraguay"
    CA: str = "http://www.cambiosalberdi.com/ws/getTablero.json.php"
    MYD: str = "https://www.mydcambios.com.py/home"
    GNB: str = "https://www.bancognb.com.py/public/currency_quotations"
    EUROC: str = "https://eurocambios.com.py/v2/sgi/utilsDto.php"
    MUNDIALC: str = "https://mundialcambios.com.py/"
    VISIONC: str = "https://www.visionbanco.com/personas/servicios/mesa-de-cambios"
    BONANZA: str = "https://www.bonanzacambios.com.py/index.php"
    LAMONEDA: str = "https://www.lamoneda.com.py/"
    YRENDAGUE: str = "https://www.yrendague.com.py/datos.php"
    TRIPLEC: str = "http://www.cambiostriplec.com.py/historico/get"

    GEN_HEADERS: dict = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    DB_NAME: str = "exchange.sqlite"
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{FP}/{DB_NAME}"

    class Config:
        case_sensitive = True


settings = Settings(_env_file=f"{FP}/settings.env", _env_file_encoding="utf-8")
