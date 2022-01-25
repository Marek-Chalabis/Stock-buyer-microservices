from src.fills import get_random_fill


def test_get_random_fill(mocker):
    mocker_choice = mocker.patch('src.fills.random.choice')
    mocker_randint = mocker.patch('src.fills.random.randint')
    mocker_uniform = mocker.patch('src.fills.random.uniform')
    assert get_random_fill() == {
        'stock_ticker': mocker_choice(),
        'price': round(mocker_uniform(), 2),
        'quantity': mocker_randint(),
    }
