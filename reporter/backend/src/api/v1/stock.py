from http import HTTPStatus

from flask import (
    Response,
    request,
)
from flask.views import MethodView

from src.api.security import token_required
from src.api.v1.schemas import StocksSchema
from src.api.v1.tasks import add_stock


class Stock(MethodView):
    decorators = [token_required]

    def post(self) -> Response:
        if errors := StocksSchema().validate(request.json):
            return Response(
                str(errors),
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        add_stock.delay(stocks=request.json)
        return Response(status=HTTPStatus.CREATED)
