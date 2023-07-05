from typing import List, Optional
from schemas.db_criterias import DBCriteria
from sqlalchemy.orm import Session
from db.g_session import db_session
from db.uw_exchange import ex_query, ex_bulk_insert
from serials.sa_models import bulk_sa_dict
from mval.mfields import validate_email
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
               order_by: list = [],
               db: Session = Depends(db_session),
    ) -> dict:
    logger.info('Execuging qs_execute')
    crt = map(lambda x: x.dict(), criteria)
    logger.info(f'Executing criteria in {module}, {model}')
    return {'msg': 'success', 
            'data': bulk_sa_dict(ex_query(db, module, model, crt, order_by=order_by))
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

@router.get("/group_sources", response_class=UJSONResponse)
def group_sources(db: Session = Depends(db_session)):
    logger.info('Get group sources')
    return {
        'msg': 'List of group sources',
        'data': list(
                ex_query(db, 
                        module='models.m_finance', 
                        model='Exchange',
                        criteria=[],
                        dst_vals=['group_source']
                    )
        )
    }

@router.get("/currencies", response_class=UJSONResponse)
def currencies(db: Session = Depends(db_session)):
    logger.info('Get currencies')
    return {
        'msg': 'List of currencies',
        'data': list(
                ex_query(db, 
                        module='models.m_finance', 
                        model='Exchange',
                        criteria=[],
                        dst_vals=['currency']
                    )
        )
    }

@router.post("/suscribe", response_class=UJSONResponse)
def suscribe(email: str, db: Session = Depends(db_session)):
    email = email.strip()
    if not validate_email(email): return {'msg': f'The {email} is not valid'}
    d = ex_query(
        db,
        module='models.m_finance',
        model='NewsExchange',
        criteria=[
            {"attr": "email", "optr": "==", "value": email},
        ],
        robj="scalar_one_or_none",
    )
    if  d: return {'msg': f'The {email} is already suscribe. If you want to unsiscribe this email, please use the /unsuscribe endpoint'}
    ex_bulk_insert(db, 'models.m_finance', 'NewsExchange', [{'email': email}])
    return {'msg': f'Successfully suscribe the email {email} for the daily exchange report'}