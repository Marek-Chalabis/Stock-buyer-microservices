from src.api.api_v1.api import api_router_v1


def test_api_router_v1_authorize():
    authorized_endpoints = {route.name for route in api_router_v1.routes}
    assert authorized_endpoints == {'splits_accounts', 'trade_fills'}
