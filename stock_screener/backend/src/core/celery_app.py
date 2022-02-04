from celery import Celery
from celery.schedules import crontab

from src.core.config import settings

celery_app = Celery(
    'worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
    include=['src.stocks.tasks'],
)
celery_app.conf.beat_schedule = {
    'send_stocks_to_reporter': {
        'task': 'send_stocks_to_reporter',
        'schedule': crontab(hour=6),
    },
}
