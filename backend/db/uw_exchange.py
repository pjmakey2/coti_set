from typing import Optional, Any
import logging
from sqlalchemy.engine.result import _RowData
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, between, extract, \
        distinct, tuple_, and_, or_, \
        Column, String, Text, Unicode, UnicodeText, \
        Date, DateTime, Time, \
        Double, Float, Integer, BigInteger, SmallInteger, Numeric
from datetime import date, datetime, time
from decimal import Decimal
from models.m_finance import Exchange
from importlib import import_module

def check_column_type(column: Column, value: Any, criteria: dict) -> dict:
    """
    For update into types go to https://docs.sqlalchemy.org/en/latest/core/types.html
        BigInteger,Integer,Float,Double,Numeric,SmallInteger
        Boolean
        Date,DateTime,Time
        Enum
        Interval
        LargeBinary
        MatchType
        PickleType
        SchemaType
        String,Text,Unicode,UnicodeText
        Uuid
    """
    emsg = 'There is an ERROR of type {error}  in COLUMN = {col} with VALUE = {val}'
    if isinstance(value, list | set):
        vns = []
        for v in value:
            r = check_column_type(column, v, criteria)
            if r.get('error'): return r
            vns.append(r.get('value'))
        return {'value': vns}

    if isinstance(column.type, String | Text | Unicode | UnicodeText):
        return {'value': value}
    if isinstance(column.type, DateTime | Date):
        if criteria.get('extract_value'):
            try:
                return {'value': int(value)}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
    if isinstance(column.type, DateTime):            
        if isinstance(value, DateTime | Date):
            return {'value': value}
        if isinstance(value, str | bytes):
            try:
                return {'value': datetime.strptime(value, '%Y-%m-%d %H:%M:%S')}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
    if isinstance(column.type, Date):
        if isinstance(value, DateTime | Date):
            return {'value': value}        
        if isinstance(value, str | bytes):
            try:
                return {'value': datetime.strptime(value, '%Y-%m-%d').date()}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
            
    if isinstance(column.type, Time):
        if isinstance(value, DateTime | Date | time):
            return {'value': value}
        if isinstance(value, str | bytes):
            try:
                return {'value': datetime.strptime(value, '%H:%M:%S')}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
    if isinstance(column.type, Float | Double):
        if isinstance(value, float | Decimal ):
            return {'value': value}
        if isinstance(value, str | bytes):
            try:
                return {'value': float(value)}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
            
    if isinstance(column.type, Integer | SmallInteger | BigInteger | Numeric):
        if isinstance(value, int ):
            return {'value': value}
        if isinstance(value, str | bytes):
            try:
                return {'value': int(value)}
            except ValueError:
                return {'error': emsg.format(error='VALUE ERROR',
                                             col=column.name, 
                                             val=value)}
    return {'error': emsg.format(
        error='NOT IMPLEMENTED',
        col=column.name,
        value=value
    )}


def construct_criteria(module: str, 
                       sa_model: str, 
                       criterias: list | map) -> list:
    """Construct dynamically sqlalchemy where criterias
    Args:
        module (str): _description_
        sa_model (str): _description_
        criterias (dict): [
          {'attr': 'source', 'optr': '==', 'value': 'set'},
          {'attr': 'buy', 'optr': '>', 'value': 7120},
          {'attr': 'id', 'in': '>', 'value': [1229, 1230]},
          {'attr': 'date', 'between': '>', 'value': ['2021-01-01', '2021-01-31']},
        ]
    """
    modelobj = getattr(import_module(module), sa_model)
    crts = []
    for c in criterias:
        colobj = getattr(modelobj, c.get('attr'))
        value = c.get('value')
        rva = check_column_type(colobj, value, c)
        if rva.get('error'):
            return rva
        optr = c.get('optr')
        if optr == '==':crts.append(colobj == rva.get('value'))
        if optr == '>':crts.append(colobj > rva.get('value'))
        if optr == '>=':crts.append(colobj >= rva.get('value'))
        if optr == '<':crts.append(colobj < rva.get('value'))
        if optr == '<=':crts.append(colobj <= rva.get('value'))
        if optr == 'in':crts.append(colobj.in_(rva.get('value')))
        #stmt = select(users_table).where(between(users_table.c.id, 5, 7))
        if optr == 'between':crts.append(
                between(colobj, *rva.get('value'))
        )
        if optr == 'ilike':crts.append(
            colobj.ilike(f"%{rva.get('value')}%")
        )
        if optr == 'like':crts.append(
            colobj.like(f"%{rva.get('value')}%")
        )
        # stmt = select(logged_table.c.id).where(extract("YEAR", logged_table.c.date_created) == 2021)
        if optr == 'extract':crts.append(
            extract(c.get('extract_value'), colobj) == rva.get('value')
        )
    return crts

def ex_bulk_insert(db: Session, module: str, model: str, entries: list) -> dict:
    modelobj = getattr(import_module(module), model)
    db.execute(
        insert(modelobj),
        entries
    )
    return {'success': 'Done!!!'}

def build_distinct(attrs: list, module: str, model: str):
    modelobj = getattr(import_module(module), model)
    vv = []
    for attr in attrs:
        vv.append(getattr(modelobj, attr))
    return tuple_(*vv)

def ex_query(db: Session, 
             module:str, 
             model: str, 
             criteria: list | map, 
             dst_vals: Optional[list] = [],
             robj: str = 'scalars',
             order_by: list = [],
             limit: Optional[int] = None
             ) -> _RowData:
    qcrt = construct_criteria(module, model, criteria)
    modelobj = getattr(import_module(module), model)
    ob = []
    if order_by:
        for attr in order_by:
            if attr.startswith('-'):
                gatt = getattr(modelobj, attr.replace('-', '')).desc()
            else:
                gatt = getattr(modelobj, attr)

            ob.append(gatt)
    if dst_vals:
        dstv = build_distinct(dst_vals, module, model)
        stmt = select(distinct(dstv)).where(*qcrt).limit(limit)
    else:
        stmt = select(modelobj).where(*qcrt).order_by(*ob).limit(limit)
    stcm = stmt.compile(compile_kwargs={"literal_binds": True})
    logging.info(f'Running {stcm}')
    if robj == 'scalar_one_or_none': 
        return db.execute(stmt).scalar_one_or_none()
    return db.execute(stmt).scalars()
    
