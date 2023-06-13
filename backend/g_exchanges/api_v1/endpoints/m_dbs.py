from typing import List
from schemas.db_criterias import DBCriteria
from sqlalchemy.orm import sessionmaker
from db.g_session import db_session
from db.uw_exchange import ex_query
from serials.sa_models import bulk_sa_dict
from fastapi import APIRouter, Depends
from sqlalchemy import select
from fastapi.responses import UJSONResponse
import logging
logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post("/qs_execute", response_class=UJSONResponse)
def qs_execute(criteria: List[DBCriteria],
               module: str,
               model: str,
               db: sessionmaker = Depends(db_session), 
    ) -> dict:
    logger.info('Execuging qs_execute')
    crt = map(lambda x: x.dict(), criteria)
    logger.info(f'Executing criteria in {module}, {model}')
    with db() as ses:
        return {'msg': 'success', 
                'data': bulk_sa_dict(ex_query(ses, module, model, crt))
                }

