from typing import Optional, List
from pydantic import BaseModel


class DBCriteria(BaseModel):
    attr: str
    optr: str
    value: str | List[str]
    extract_value: Optional[str]

class GRRanking(BaseModel):
    date: str
    currency: str

