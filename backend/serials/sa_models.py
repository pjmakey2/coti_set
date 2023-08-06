from datetime import datetime, date
from decimal import Decimal

def sa_encoder(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Decimal):
        return float(obj)
    
def bulk_sa_dict(scalars) -> list:
    return [ sa_dict(r)  for r in scalars]

def sa_dict(obj) -> dict:
    if hasattr(obj, '__dict__'):
        ddi = obj.__dict__
        ddi.pop('_sa_instance_state', None)
        return ddi
    if hasattr(obj, '_asdict'):
        return obj._asdict()
    raise NotImplementedError('There is no implementation for converting {} to a dict'.format(obj))

