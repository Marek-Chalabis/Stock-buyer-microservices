import numpy

from src.accounts_split.accounts import (
    AccountsSplits,
    get_accounts,
)


def test_get_accounts():
    assert get_accounts() == [
        'Account_1',
        'Account_2',
        'Account_3',
        'Account_4',
        'Account_5',
        'Account_6',
        'Account_7',
        'Account_8',
        'Account_9',
        'Account_10',
    ]


class TestAccountsSplitData:
    def test_get_random_accounts(self, mocker):
        mocker_get_accounts = mocker.patch('src.accounts_split.accounts.get_accounts')
        mocker_sample = mocker.patch(
            'src.accounts_split.accounts.random.sample',
            return_value=True,
        )
        tested_random_number_of_accounts = 1
        assert AccountsSplits()._get_random_accounts(1)
        mocker_sample.assert_called_once_with(
            mocker_get_accounts(),
            tested_random_number_of_accounts,
        )

    def test_get_random_splits_percents(self, mocker):
        mocker_ones = mocker.patch(
            'src.accounts_split.accounts.numpy.ones',
            return_value=1,
        )
        mocker_multinomial = mocker.patch(
            'src.accounts_split.accounts.numpy.random.multinomial',
            return_value=numpy.array([1]),
        )
        assert AccountsSplits()._get_random_splits_percents(1) == 1
        mocker_ones.assert_called_with(1)
        mocker_multinomial.assert_called_once_with(n=100, pvals=1.0, size=1)

    def test_get_random_accounts_splits(self, mocker):
        mocker.patch(
            'src.accounts_split.accounts.AccountsSplits._get_random_accounts',
            return_value=['a', 'b'],
        )
        mocker.patch(
            'src.accounts_split.accounts.AccountsSplits._get_random_splits_percents',
            return_value=[1, 2],
        )
        assert AccountsSplits().get_random_accounts_splits() == {'a': 1, 'b': 2}
