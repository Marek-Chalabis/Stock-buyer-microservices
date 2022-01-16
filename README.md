# Stock-buyer-microservices

WIP -> currently on aum_server

TODO:

aum_server:
- implement httpx for async calls to controller

controller:
- add tokens to aum_server
- add to code -> @validate_arguments
- add DB (redis probably) for keeping accounts percents and tokens
- ??remove if __name__ == "__main__" for production??
- create trade_share network
- add flower to monitor fastapi
