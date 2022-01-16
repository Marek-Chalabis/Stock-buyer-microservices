from src.accounts.account_split_data import AccountsSplitData
from src.celery import celery_app


@celery_app.task(name='send_account_split_to_controller')
def send_account_split_to_controller() -> None:
    accounts_split_data = AccountsSplitData().get_random_account_split_data()
    # TODO send to controller
    print(accounts_split_data)
