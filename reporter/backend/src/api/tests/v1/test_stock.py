from http import HTTPStatus

from src.api.security import token_required
from src.api.v1.stock import Stock


class TestStock:
    def test_decorators(self):
        assert Stock.decorators == [token_required]

    def test_post_validation_called(self, mocker):
        mocker_validate = mocker.patch('src.api.v1.stock.StocksSchema.validate')
        Stock().post()
        mocker_validate.assert_called_once_with(
            None,
        )

    def test_post_wrong_validation(self, mocker):
        mocker.patch(
            'src.api.v1.stock.StocksSchema',
            return_value=mocker.Mock(
                validate=mocker.Mock(return_value={'test': 'test'}),
            ),
        )
        tested_response = Stock().post()
        assert tested_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert tested_response.data == b"{'test': 'test'}"

    def test_post_task_called(self, mocker):
        mocker_add_stock = mocker.patch('src.api.v1.stock.add_stock.delay')
        mocker.patch(
            'src.api.v1.stock.StocksSchema',
            return_value=mocker.Mock(
                validate=mocker.Mock(return_value={}),
            ),
        )
        Stock().post()
        mocker_add_stock.assert_called_once_with(stocks=None)

    def test_post_response(self, mocker):
        mocker.patch(
            'src.api.v1.stock.StocksSchema',
            return_value=mocker.Mock(
                validate=mocker.Mock(return_value={}),
            ),
        )
        assert Stock().post().status_code == HTTPStatus.CREATED
