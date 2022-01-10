# Stock-buyer-microservices

WIP -> currently on aum_server

taaa

TODO:

aum_server:
- implement httpx for async calls to controller
- add logger
- divide dependencies develop/production
- create separate docker-compose files for prod/develop
- auto update for packages and check from poetry
- add flower for celery workers
- modify APP_STATUS
- fix packagen dependencies in pyproject

controller:
- add to code -> @validate_arguments
- add DB (redis probably) for keeping accounts percents and tokens
- ??remove if __name__ == "__main__" for production??
- create trade_share network
