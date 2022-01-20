from src.celery import env

CONTROLLER_SERVER_API_V1_URL = env('CONTROLLER_SERVER_API_V1_URL')
CONTROLLER_SERVER_CLIENT = {  # noqa: WPS407
    'account-split': f'{CONTROLLER_SERVER_API_V1_URL}/account-split/',
}
