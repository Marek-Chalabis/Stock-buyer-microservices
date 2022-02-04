import random

import httpx

from src.core.celery_app import celery_app
from src.core.config import settings
from src.core.external_services_endpoints import external_endpoints
from src.stocks.stock import generate_random_stocks


@celery_app.task(name='send_stocks_to_reporter')
def send_stocks_to_reporter() -> None:
    url = external_endpoints.reporter['stocks']
    number_of_random_stocks = random.randint(1, 20)  # noqa: S311
    random_stocks = generate_random_stocks(
        number_of_stocks=number_of_random_stocks,
    )  # noqa: S311
    httpx.post(
        url=url,
        json={'stocks': random_stocks},
        headers={'x-api-key': settings.REPORTER_TOKEN},
    )
