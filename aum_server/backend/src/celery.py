from environs import Env

from celery import Celery
from celery.utils.log import get_task_logger
from src.constants import INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC

env: Env = Env()
Env.read_env()

CELERY_BROKER_URL: str = env('CELERY_BROKER_URL')
CONTROLLER_SERVER_API_V1_URL: str = env('CONTROLLER_SERVER_API_V1_URL')

celery_app = Celery(
    'celery',
    broker=CELERY_BROKER_URL,
    include=['src.periodic_tasks.tasks'],
)

logger = get_task_logger(__name__)
logger.setLevel('ERROR')

celery_app.conf.beat_schedule = {
    'send_account_split_to_controller': {
        'task': 'send_account_split_to_controller',
        'schedule': INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC,
    },
}
