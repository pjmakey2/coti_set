from fastapi import FastAPI
import logging, os
#from starlette.middleware.cors import CORSMiddleware
from g_exchanges.api_v1.api import api_router
from sts import settings as sst
FP = os.path.realpath(os.path.curdir)
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__) 
logger.info(f'Starting {sst.PROJECT_NAME} API VERSION {sst.VERSION}')
app = FastAPI(title=sst.PROJECT_NAME)
app.include_router(api_router, prefix=sst.VERSION)
logger.info(f'Starting {sst.PROJECT_NAME} API VERSION {sst.VERSION}')
