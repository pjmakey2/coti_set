from typing import List
from schemas.db_criterias import DBCriteria
from sqlalchemy.orm import Session
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
               db: Session = Depends(db_session),
    ) -> dict:
    logger.info('Execuging qs_execute')
    crt = map(lambda x: x.dict(), criteria)
    logger.info(f'Executing criteria in {module}, {model}')
    return {'msg': 'success', 
            'data': bulk_sa_dict(ex_query(db, module, model, crt))
    }

@router.get("/sources", response_class=UJSONResponse)
def sources(db: Session = Depends(db_session)):
    logger.info('Get sources')
    return {
        'msg': 'List of exchange sources',
        'data': list(
                ex_query(db, 
                        module='models.m_finance', 
                        model='Exchange',
                        criteria=[],
                        dst_vals=['source']
                    )
        )
    }