from src.api.schemas import AccountsSplits


def test_accounts_splits_super_dict():
    accounts_splits = AccountsSplits.parse_obj({'test': 1})
    assert accounts_splits.dict() == {'test': 1.0}
