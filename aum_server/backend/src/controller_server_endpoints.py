from src.celery import CONTROLLER_SERVER_API_V1_URL

CONTROLLER_SERVER_CLIENT = {  # noqa: WPS407
    'account-split': f'{CONTROLLER_SERVER_API_V1_URL}/account-split/',
}
