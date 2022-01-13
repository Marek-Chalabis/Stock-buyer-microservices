import random

from typing import (
    Dict,
    List,
)

import numpy

from src.accounts.constants import NUMBER_OF_ACCOUNTS


class AccountsSplitData:
    @property
    def accounts(self, number_of_accounts=NUMBER_OF_ACCOUNTS) -> List[str]:
        return [f'Account_{index}' for index in range(1, number_of_accounts + 1)]

    def _get_random_accounts(self, random_number_of_accounts: int) -> List[str]:
        return random.choices(self.accounts, k=random_number_of_accounts)

    def _get_random_splits_percents(
        self, random_number_of_accounts: int
    ) -> List[float]:
        pvals = numpy.ones(random_number_of_accounts) / random_number_of_accounts
        return numpy.random.multinomial(n=100, pvals=pvals, size=1)[0]

    def get_random_account_split_data(self) -> Dict[str, float]:
        """Returns x number of accounts with split percentage summed to 100."""
        random_number_of_accounts = random.randint(1, NUMBER_OF_ACCOUNTS)
        accounts = self._get_random_accounts(
            random_number_of_accounts=random_number_of_accounts
        )
        splits = self._get_random_splits_percents(
            random_number_of_accounts=random_number_of_accounts
        )
        return dict(zip(accounts, splits))
