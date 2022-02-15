from api.v1 import api_v1
from api.v1.stock import Stock


# TODO token, remove get from endpoint

stocks_view = Stock.as_view('stocks_api')
api_v1.add_url_rule('/stocks', methods=['POST', 'GET'], view_func=stocks_view)