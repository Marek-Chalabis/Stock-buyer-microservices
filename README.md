# Stock-buyer-microservices

> Connected microservices/app to handle and report stock trade fills

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

- [Aum server](aum_server): Microservice responsible for splitting trade shares

- [Fill server](fill_server): Microservice responsible for creating fill trades

- [Controller server](controller_server): Microservice responsible for creating stock 
purchase order from gathered data and sending them to position server

- [Reporter](reporter): WIP

## Setup

1 Install Docker and Docker compose

2 Adjust environment variables in [
    [Aum server](aum_server/config/environment_variables/.env),
    [Fill server](fill_server/config/environment_variables/.env),
    [Controller server](controller_server/config/environment_variables/.env),
    [Reporter](reporter/config/environment_variables/.env),
] or run with default ones

3 Create a network to allow microservices/app to communicate

```
    docker network create stock_buyer_network
```

4 Build images
```
    docker-compose -f fill_server/docker-compose.yaml -f controller_server/docker-compose.yaml -f aum_server/docker-compose.yaml build
```

5 Run containers
```
    docker-compose -f controller_server/docker-compose.yaml up -d && docker-compose -f aum_server/docker-compose.yaml up -d && docker-compose -f fill_server/docker-compose.yaml up -d
```

## Tests
```
    docker-compose -f fill_server/docker-compose.yaml run --rm app make full_test_code && docker-compose -f aum_server/docker-compose.yaml run --rm app make full_test_code && docker-compose -f controller_server/docker-compose.yaml run --rm app make full_test_code
```

## Technologies

- Python 
- FastAPI 
- Redis
- Celery

## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com

## TODO
aum server:
- add link to api documentation
- adjust/fix logger

controller:
- add link to api documentation
- adjust/fix logger
- Add CORS

fill server:
- add link to api documentation
- adjust/fix logger