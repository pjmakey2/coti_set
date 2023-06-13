from typing import Optional, Any
from sqlalchemy.engine import ScalarResult
from sqlalchemy import select, insert, between, extract, \
        Column, String, Text, Unicode, UnicodeText, \
        Date, DateTime, Time, \
        Double, Float, Integer, BigInteger, SmallInteger, Numeric
from datetime import date, datetime, time
from decimal import Decimal
from models.m_finance import Exchange
from db.g_session import Session
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
        print(rva)
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


def check_exchange(source: str, currency: str,sales: float | int,buy: float | int,odate: date | datetime) -> Optional[Any]:
    if isinstance(date, datetime):
        odate = odate.date()
    with Session() as ss:
        return ss.execute(
           select(Exchange).filter(
                    Exchange.source == source,
                    Exchange.currency == currency,
                    Exchange.sales == sales,
                    Exchange.buy == buy,
                    Exchange.date == odate,
            )
         ).scalar_one_or_none()
    
def save_exchanges(exchanges: list) -> dict:
    with Session() as ss:
         ss.execute(
              insert(Exchange),
              exchanges
         )
    return {'success': 'Done!!!'}

def get_exchanges(criteria: list) -> ScalarResult:
    qcrt = construct_criteria('m_finance.models', 'Exchange', criteria)
    stmt = select(Exchange).where(*qcrt)
    with Session() as session:
        return session.execute(stmt).scalars()
    
