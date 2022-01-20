import httpx

from src.accounts.account_split_data import AccountsSplitData
from src.celery import (
    celery_app,
    env,
    logger,
)
from src.controller_server_endpoints import CONTROLLER_SERVER_CLIENT

CONTROLLER_SERVER_KEY_SECRET = env('CONTROLLER_SERVER_KEY_SECRET')


@celery_app.task(name='send_account_split_to_controller')
def send_account_split_to_controller() -> None:
    accounts_split_data = AccountsSplitData().get_random_account_split_data()
    endpoint = CONTROLLER_SERVER_CLIENT['account-split']
    response = httpx.post(
        endpoint,
        json=accounts_split_data,
        headers={'x-api-key': CONTROLLER_SERVER_KEY_SECRET},
    )
    if response.status_code == httpx.codes.ACCEPTED:
        logger.error(
            'Request to url: "{0}" not accepted with data:\n{1}'.format(
                endpoint,
                accounts_split_data,
            ),
        )
