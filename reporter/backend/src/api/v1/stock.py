from flask import (
    Response,
    request,
)
from flask.views import MethodView

from src.api.security import token_required
from src.api.v1.schemas import StocksSchema
from src.api.v1.tasks import add_stock

stocks_schema = StocksSchema()


class Stock(MethodView):
    decorators = [token_required]

    def post(self) -> Response:
        if errors := stocks_schema.validate(request.json):
            return Response(str(errors), status=422)  # TODO check for type
        add_stock.delay(stocks=request.json)
        return Response(status=201)
