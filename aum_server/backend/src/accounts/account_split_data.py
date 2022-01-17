import random

from functools import lru_cache
from typing import (
    Dict,
    List,
)

import numpy

from src.accounts.constants import NUMBER_OF_ACCOUNTS


@lru_cache(maxsize=1)
def accounts(number_of_accounts: int = NUMBER_OF_ACCOUNTS) -> List[str]:
    return [f'Account_{index}' for index in range(1, number_of_accounts + 1)]


class AccountsSplitData:

    def get_random_account_split_data(self) -> Dict[str, float]:
        """X number of accounts with split percentage summed to 100."""
        random_number_of_accounts = random.randint(1, NUMBER_OF_ACCOUNTS)  # noqa: S311
        random_accounts = self._get_random_accounts(
            random_number_of_accounts=random_number_of_accounts,
        )
        random_splits = self._get_random_splits_percents(
            random_number_of_accounts=random_number_of_accounts,
        )
        return dict(zip(random_accounts, random_splits))

    def _get_random_accounts(self, random_number_of_accounts: int) -> List[str]:
        return random.choices(accounts(), k=random_number_of_accounts)  # noqa: S311

    def _get_random_splits_percents(
        self,
        random_number_of_accounts: int,
    ) -> List[float]:
        pvals = numpy.ones(random_number_of_accounts) / random_number_of_accounts
        numpy_multidimensional_array = numpy.random.multinomial(
            n=100,
            pvals=pvals,
            size=1,
        )
        return numpy_multidimensional_array[0].tolist()
