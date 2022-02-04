from src.stocks.stock import (
    Stock,
    generate_random_stocks,
)


def test_generate_random_stocks(mocker):
    mock_stock = mocker.patch(
        'src.stocks.stock.Stock',
        return_value=Stock(
            symbol='test',
            name='test',
            price=1,
            quantity=1,
        ),
    )
    tested_result = generate_random_stocks(1)
    mock_stock.assert_called_once()
    assert tested_result == [
        {'name': 'test', 'price': 1, 'quantity': 1, 'symbol': 'test'},
    ]
