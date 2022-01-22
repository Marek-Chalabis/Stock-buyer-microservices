import httpx

from src import settings
from src.accounts_split.accounts import AccountsSplits
from src.celery import (
    celery_app,
    logger,
)


@celery_app.task(name='send_accounts_splits_to_controller')
def send_accounts_splits_to_controller() -> None:
    accounts_splits_data = AccountsSplits().get_random_accounts_splits()
    endpoint = settings.CONTROLLER_SERVER_CLIENT['accounts-splits']
    response = httpx.post(
        endpoint,
        json=accounts_splits_data,
        headers={'x-api-key': settings.CONTROLLER_SERVER_KEY_SECRET},
    )
    if response.status_code != httpx.codes.ACCEPTED:
        logger.error(
            'Request to url: "{0}" not accepted with data:\n{1}'.format(
                endpoint,
                accounts_splits_data,
            ),
        )
