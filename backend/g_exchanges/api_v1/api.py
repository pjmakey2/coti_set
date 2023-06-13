from fastapi import APIRouter
from g_exchanges.api_v1.endpoints import m_dbs

api_router = APIRouter()
api_router.include_router(m_dbs.router, 
                          prefix="/retrieve", 
                          tags=["retrieve"])
