from trades import trades
from trades.view import TradesView

trades.add_url_rule('/trades', view_func=TradesView.as_view('trades_page'))
