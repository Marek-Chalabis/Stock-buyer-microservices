from types import MappingProxyType

from environs import Env

from celery.utils.log import get_task_logger

env: Env = Env()
Env.read_env()

CELERY_BROKER_URL: str = env('CELERY_BROKER_URL')
CONTROLLER_SERVER_KEY_SECRET: str = env('CONTROLLER_SERVER_KEY_SECRET')
CONTROLLER_SERVER_API_V1_URL: str = env('CONTROLLER_SERVER_API_V1_URL')
CONTROLLER_SERVER_CLIENT = MappingProxyType(
    {
        'trade-fills': f'{CONTROLLER_SERVER_API_V1_URL}/trade-fills/',
    },
)

logger = get_task_logger(__name__)
