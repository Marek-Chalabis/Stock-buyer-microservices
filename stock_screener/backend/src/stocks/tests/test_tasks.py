from src.stocks.tasks import send_stocks_to_reporter


def test_send_stocks_to_reporter(mocker):
    mock_settings = mocker.patch('src.stocks.tasks.settings')
    mock_settings.REPORTER_TOKEN = 'test_reporter_token'
    mock_external_endpoints = mocker.patch(
        'src.stocks.tasks.external_endpoints',
    )
    mock_external_endpoints.reporter = {'stocks': 'test_url'}
    mock_randint = mocker.patch('src.stocks.tasks.random.randint')
    mock_generate_random_stocks = mocker.patch(
        'src.stocks.tasks.generate_random_stocks',
    )
    mock_httpx_post = mocker.patch('src.stocks.tasks.httpx.post')

    send_stocks_to_reporter()
    mock_generate_random_stocks.assert_called_once_with(number_of_stocks=mock_randint())
    mock_httpx_post.assert_called_once_with(
        url='test_url',
        json={'stocks': mock_generate_random_stocks()},
        headers={'x-api-key': mock_settings.REPORTER_TOKEN},
    )
