import httpx

from src.celery import (
    celery_app,
    env,
    logger,
)
from src.controller_server_endpoints import CONTROLLER_SERVER_CLIENT
from src.fills.fills import get_random_fill

CONTROLLER_SERVER_KEY_SECRET = env('CONTROLLER_SERVER_KEY_SECRET')


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
