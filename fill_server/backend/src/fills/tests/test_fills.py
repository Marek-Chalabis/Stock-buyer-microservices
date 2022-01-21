from src.fills.fills import get_random_fill


def test_get_random_fill(mocker):
    mocker_random = mocker.patch('src.fills.fills.random.choice')
    mocker_quantity = mocker.patch('src.fills.fills.random.randint')
    mocker_price = mocker.patch('src.fills.fills.random.uniform')
    assert get_random_fill() == {
        'stock_ticker': mocker_random(),
        'price': round(mocker_price(), 2),
        'quantity': mocker_quantity(),
    }
