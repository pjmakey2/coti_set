from typing import Generator
import logging
from sts import settings as sst
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine

logger = logging.getLogger(__name__) 

engine = create_engine(
        sst.SQLALCHEMY_DATABASE_URI,
        echo=sst.DEBUG
)
logger.info(f'Initiate a session to the database {sst.SQLALCHEMY_DATABASE_URI}')
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def db_session() -> Generator:
    try:
        dbs = Session
        yield dbs
        dbs.commit()
    except Exception as e:
        logger.info(f'There was an error in the session ERROR={e}')

