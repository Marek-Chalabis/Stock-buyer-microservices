from fastapi import APIRouter

from src.api.v1 import stocks

api_router = APIRouter()
api_router.include_router(stocks.router, prefix='/stocks', tags=['stocks'])
