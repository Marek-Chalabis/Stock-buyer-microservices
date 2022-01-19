from fastapi import APIRouter

from src.api.api_v1.endpoints import account_split

api_router_v1 = APIRouter()
api_router_v1.include_router(account_split.router, prefix="/account-split", tags=["account-split"])