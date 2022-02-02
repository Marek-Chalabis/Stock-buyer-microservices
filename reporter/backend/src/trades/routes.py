from flask_login import login_required

from trades import trades


@trades.route('/trades')
@login_required
def trades_page():
    return 'TODO Trades'
