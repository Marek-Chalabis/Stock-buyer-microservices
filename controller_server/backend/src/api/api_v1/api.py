from fastapi import (
    APIRouter,
    Depends,
)

from src.api.api_v1.endpoints import (
    account_split,
    fills,
)
from src.api.authorize import AuthorizerDependencyByXApiKey

authorizer = AuthorizerDependencyByXApiKey()
api_router_v1 = APIRouter(dependencies=[Depends(authorizer)])

api_router_v1.include_router(
    account_split.router,
    prefix='/accounts-splits',
    tags=['accounts-splits'],
)
api_router_v1.include_router(
    fills.router,
    prefix='/trade-fills',
    tags=['trade-fills'],
)
