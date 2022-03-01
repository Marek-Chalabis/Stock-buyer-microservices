from src.trades import trades
from src.trades.view import TradesView

trades.add_url_rule('/trades', view_func=TradesView.as_view('trades_page'))
