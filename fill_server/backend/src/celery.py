import random
import time

import httpx

from environs import Env

from celery import Celery
from celery.utils.log import get_task_logger
from src.constants import (
    MAX_SEND_TRADE_FILL_INTERVAL,
    MIN_SEND_TRADE_FILL_INTERVAL,
)
from src.fills import get_random_fill

env: Env = Env()
Env.read_env()

CELERY_BROKER_URL: str = env('CELERY_BROKER_URL')
CONTROLLER_SERVER_KEY_SECRET: str = env('CONTROLLER_SERVER_KEY_SECRET')
CONTROLLER_SERVER_API_V1_URL: str = env('CONTROLLER_SERVER_API_V1_URL')
CONTROLLER_SERVER_CLIENT = {
    'fills': f'{CONTROLLER_SERVER_API_V1_URL}/fills/',
}
celery_app = Celery(
    'celery',
    broker=CELERY_BROKER_URL,
)

logger = get_task_logger(__name__)
logger.setLevel('ERROR')


@celery_app.task
def send_trade_fill_to_controller() -> None:
    trade_fill = get_random_fill()
    endpoint = CONTROLLER_SERVER_CLIENT['fills']
    response = httpx.post(
        endpoint,
        json=trade_fill,
        headers={'x-api-key': CONTROLLER_SERVER_KEY_SECRET},
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
    while True:
        random_sleep = random.randint(
            MIN_SEND_TRADE_FILL_INTERVAL, MAX_SEND_TRADE_FILL_INTERVAL
        )
        time.sleep(random_sleep)
        send_trade_fill_to_controller.delay()


#  this is hacky, if there is gonna be more tasks
#  implement flask for handling more complex tasks logic
send_trade_fill_to_controller_random.delay()
