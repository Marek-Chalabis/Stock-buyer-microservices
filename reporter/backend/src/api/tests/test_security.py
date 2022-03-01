from src.api.security import token_required


@token_required
def token_required_test_func(*args, **kwargs):
    return args, kwargs


def test_token_required_no_header(mocker):
    mocker.patch('src.api.security.request.headers.get', return_value='test')
    response = token_required_test_func()
    assert response.status_code == 403


def test_token_required_wrong_secret_key(mocker):
    mocker.patch('src.api.security.request.headers.get', return_value='test')
    mocker.patch(
        'src.api.security.BaseConfig.SECRET_KEY',
        new_callable=mocker.PropertyMock,
        return_value='wrong_secret_key',
    )
    response = token_required_test_func()
    assert response.status_code == 403


def test_token_required_correct(mocker):
    mocker.patch('src.api.security.request.headers.get', return_value='test')
    mocker.patch(
        'src.api.security.BaseConfig.SECRET_KEY',
        new_callable=mocker.PropertyMock,
        return_value='test',
    )
    response = token_required_test_func('test1', test2='test2')
    assert response == (('test1',), {'test2': 'test2'})
