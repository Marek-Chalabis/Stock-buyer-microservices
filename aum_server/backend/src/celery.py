from celery import Celery
from celery.utils.log import get_task_logger
from src import settings
from src.constants import INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC

celery_app = Celery(
    'celery',
    broker=settings.CELERY_BROKER_URL,
    include=['src.accounts_split.tasks'],
)

logger = get_task_logger(__name__)
logger.setLevel('ERROR')

celery_app.conf.beat_schedule = {
    'send_accounts_splits_to_controller': {
        'task': 'send_accounts_splits_to_controller',
        'schedule': INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC,
    },
}
