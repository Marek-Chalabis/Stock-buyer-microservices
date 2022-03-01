from src.api.v1 import api_v1
from src.api.v1.stock import Stock

stocks_view = Stock.as_view('stocks_api')
api_v1.add_url_rule('/stocks', methods=['POST'], view_func=stocks_view)
