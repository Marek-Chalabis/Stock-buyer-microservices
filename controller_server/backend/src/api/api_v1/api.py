from fastapi import (
    APIRouter,
    Depends,
)

from src.api.api_v1.authorize import AuthorizerDependencyByXApiKey
from src.api.api_v1.endpoints import account_split
from src.api.api_v1.endpoints import fills

api_router_v1 = APIRouter()
authorizer = AuthorizerDependencyByXApiKey()
api_router_v1.include_router(
    account_split.router,
    prefix='/accounts-splits',
    tags=['accounts-splits'],
    dependencies=[Depends(authorizer)],
)
api_router_v1.include_router(
    fills.router,
    prefix='/trade-fills',
    tags=['trade-fills'],
    dependencies=[Depends(authorizer)],
)