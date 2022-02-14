# Stock-buyer-microservices

> Project is still under development

> Connected microservices and reporter app to handle and report stock trade fills

## Table of contents

- [General info](#general-info)
- [Setup](#setup)
- [Tests](#tests)
- [Technologies](#technologies)
- [Contact](#contact)
- [TODO](#todo)

## General info

Projected aimed to simulate the flow of stock exchange transactions and their reporting.
This is done by connecting separate services into one network.
(services should be in different repos but for readability they are under one repo):

- [Reporter](reporter): The core of the project, connects all services and enables trades manually or by a bot

- [Stock Screener](stock_screener): Microservice responsible for stock creation

These microservices will be changed or adjusted to reporter logic.

- [Aum server](aum_server): Microservice responsible for splitting trade shares

- [Fill server](fill_server): Microservice responsible for creating fill trades

- [Controller server](controller_server): Microservice responsible for creating stock 
purchase order from gathered data and sending them to position server

## Setup

1 Install Docker and Docker compose

2 Adjust environment variables in [
    [Reporter](reporter/config/environment_variables/),
    [Stock Screener](stock_screener/config/environment_variables/)
] or run with default ones

3 Create a network to allow microservices/app to communicate

```
    docker network create stock_buyer_network
```

4 Build images
```
    docker-compose -f reporter/docker-compose.yaml -f stock_screener/docker-compose.yaml build
```

5 Run containers
```
    docker-compose -f reporter/docker-compose.yaml up -d && docker-compose -f stock_screener/docker-compose.yaml up -d
```

## Tests
```
    docker-compose -f stock_screener/docker-compose.yaml run --rm app make full_test_code && docker-compose -f reporter/docker-compose.yaml run --rm app make full_test_code
```

## Technologies

- Python
- Flask
- FastAPI 
- SQLAlchemy 
- Pytest
- Docker
- Docker-Compose
- PostgreSQL
- Redis
- Celery

## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com
