from fastapi import status


def test_stocks_status(client):
    response = client.get('/api/v1/stocks')
    assert response.status_code == status.HTTP_200_OK


def test_stocks_generate_random_stocks_call(mocker, client):
    mocker_generate_random_stocks = mocker.patch(
        'src.api.v1.stocks.generate_random_stocks',
        return_value=[],
    )
    client.get('/api/v1/stocks?number_of_stocks=1')
    mocker_generate_random_stocks.assert_called_once_with(number_of_stocks=1)
