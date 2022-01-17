import numpy

from src.accounts.account_split_data import (
    AccountsSplitData,
    accounts,
)


def test_accounts():
    assert accounts() == [
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
        mocker_accounts = mocker.patch('src.accounts.account_split_data.accounts')
        mocker_choices = mocker.patch(
            'src.accounts.account_split_data.random.choices',
            return_value=True,
        )
        tested_random_number_of_accounts = 1
        assert AccountsSplitData()._get_random_accounts(1)
        mocker_choices.assert_called_once_with(
            mocker_accounts(),
            k=tested_random_number_of_accounts,
        )

    def test_get_random_splits_percents(self, mocker):
        mocker_ones = mocker.patch(
            'src.accounts.account_split_data.numpy.ones',
            return_value=1,
        )
        mocker_multinomial = mocker.patch(
            'src.accounts.account_split_data.numpy.random.multinomial',
            return_value=numpy.array([1]),
        )
        assert AccountsSplitData()._get_random_splits_percents(1) == 1
        mocker_ones.assert_called_with(1)
        mocker_multinomial.assert_called_once_with(n=100, pvals=1.0, size=1)

    def test_get_random_account_split_data(self, mocker):
        mocker.patch(
            'src.accounts.account_split_data.AccountsSplitData._get_random_accounts',
            return_value=['a', 'b'],
        )
        mocker.patch(
            'src.accounts.account_split_data.AccountsSplitData.'
            + '_get_random_splits_percents',
            return_value=[1, 2],
        )
        assert AccountsSplitData().get_random_account_split_data() == {'a': 1, 'b': 2}
