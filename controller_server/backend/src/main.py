from fastapi import (
    APIRouter,
    FastAPI,
)

from src.api.api_v1.api import api_router_v1
from src.core.config import settings

root_router = APIRouter()
app = FastAPI(title='Controller API', openapi_url='/openapi.json')
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
app.include_router(root_router)
