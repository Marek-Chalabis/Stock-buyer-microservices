import os

from dotenv import load_dotenv

from celery import Celery
from src.constants import INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC

load_dotenv()
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
celery_app = Celery(
    'celery',
    broker=CELERY_BROKER_URL,
    include=['src.periodic_tasks.tasks'],
)

celery_app.conf.beat_schedule = {
    'send_account_split_to_controller': {
        'task': 'send_account_split_to_controller',
        'schedule': INTERVAL_FOR_SENDING_DATA_TO_CONTROLLER_SEC,
    },
}
