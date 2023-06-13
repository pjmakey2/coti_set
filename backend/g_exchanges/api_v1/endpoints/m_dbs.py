from typing import List
from schemas.db_criterias import DBCriteria
from models.m_finance import Exchange
from db.g_session import db_session
from db.uw_exchange import construct_criteria
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from fastapi.responses import UJSONResponse
import logging
logger = logging.getLogger(__name__) 

router = APIRouter()

@router.post("/qs_execute", response_class=UJSONResponse)
def qs_execute(criteria: List[DBCriteria],
               module: str,
               model: str,
               db = Depends(db_session), 
    ) -> dict:
    logger.info('Execuging qs_execute')
    # print(criteria,
    #       type(criteria),
    #     #   criteria.dict(),
    #       module,
    #       model,
    #       sep='\n')
    crt = map(lambda x: x.dict(), criteria)
    qcrt = construct_criteria(module, model, crt)
    stmt = select(Exchange).where(*qcrt)
    logger.info(f'Executing criteria in {module}, {model}')
    # stcm = str(stmt.compile(compile_kwargs={"literal_binds": True}))
    with db() as ses:
        return {'msg': 'success', 'data': ses.execute(stmt).scalars()}

