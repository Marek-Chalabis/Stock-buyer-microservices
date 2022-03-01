from http import HTTPStatus


def test_logout_page_status(client, token_header, mocker):
    mocker.patch(
        'src.api.v1.stock.StocksSchema',
        return_value=mocker.Mock(
            validate=mocker.Mock(return_value={}),
        ),
    )
    response = client.post('api/v1/stocks', data={}, headers=token_header)
    assert response.status_code == HTTPStatus.CREATED
