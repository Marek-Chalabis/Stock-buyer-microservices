import random
import time

import httpx

from celery import Celery
from celery.utils.log import get_task_logger
from src import settings
from src.constants import (
    MAX_SEND_TRADE_FILL_INTERVAL,
    MIN_SEND_TRADE_FILL_INTERVAL,
)
from src.fills import get_random_fill

celery_app = Celery(
    'celery',
    broker=settings.CELERY_BROKER_URL,
)

logger = get_task_logger(__name__)
logger.setLevel('ERROR')


@celery_app.task
def send_trade_fill_to_controller() -> None:
    trade_fill = get_random_fill()
    endpoint = settings.CONTROLLER_SERVER_CLIENT['trade-fills']
    response = httpx.post(
        endpoint,
        json=trade_fill,
        headers={'x-api-key': settings.CONTROLLER_SERVER_KEY_SECRET},
    )
    if response.status_code != httpx.codes.ACCEPTED:
        logger.error(
            'Request to url: "{0}" not accepted with data:\n{1}'.format(
                endpoint,
                trade_fill,
            ),
        )


@celery_app.task
def send_trade_fill_to_controller_random() -> None:
    """Start other tasks by random amount of time."""
    while True:  # noqa: WPS457
        random_sleep = random.randint(  # noqa: S311
            MIN_SEND_TRADE_FILL_INTERVAL,
            MAX_SEND_TRADE_FILL_INTERVAL,
        )
        time.sleep(random_sleep)
        send_trade_fill_to_controller.delay()


#  this is hacky, if there is gonna be more tasks
#  implement flask for handling more complex tasks logic
send_trade_fill_to_controller_random.delay()
