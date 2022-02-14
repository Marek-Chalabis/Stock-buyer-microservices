# Reporter
> App responsible for the management of stock trades

## Table of contents

- [General info](#general-info)
- [API documentation](#api-documentation)
- [Setup](#setup) 
- [Develop Setup](#develop setup) 
- [Tests](#tests)
- [Code format](#code-format)
- [Technologies](#technologies)
- [TODO](#todo)
- [Contact](#contact)

## General info
The Reporter is keeping track of trades held by each account and the ones
that are ready to buy. Allowing users to trade stocks manually or by using bot. 
Provides api for other microservices in network. 

## API documentation TODO not implemented
Documentation for API can found at this endpoints after running container:

- `/docs/` : Documentation endpoint 

## Setup

1 Install Docker

2 Adjust environment variables in [.env](config/environment_variables/.env)

3 Change USER_ID arg in [docker-compose.yaml](docker-compose.yaml) if your local UID is different then 1000, this will fix local file permissions.

You can check this by
```
    echo $UID
```
4 Build images (*all commands should be done in project root directory)
```
    docker-compose build
```
5 Run containers
```
    docker-compose up
```

## Develop Setup

To create DB with random data use follow command:
```
    docker-compose exec app python src/manage.py create_new_develop_db_with_random_data
``` 
## Tests
```
    docker-compose run --rm app make full_test_code
```

## Code format
```
    docker-compose run --rm app make full_format_code
```

## Technologies

- Python 
- Flask
- SQLAlchemy
- Jinja
- JavaScript
- Bootstrap
- [Python packages](backend/pyproject.toml)

## TODO

Monster tasks:

- Add frontend framework

Big tasks:

- Implement API for microservices
- Divides settings/env for prod and develop
- Add auto trade option for users, by switch on model
- Add an image for user avatar, also enable changing it
- Add migrations (alembic)
- Implement FastAPI for API side of application (FastAPI will be a main server graphql?)
- Implement Celery/redis for tasks 
- Add auto population DB with users stock fills and trades
- Implement better security on between containers in network
- Fix js to be "better/quicker"
- Fix code for mypy

Medium tasks:

- Add logic for selling trades
- Add entrypoint for DC (wait for DB, https://testdriven.io/courses/fastapi-celery/docker/)
- Allow password change
- Add script for postgresql wait on docker compose up
- Security: microservices <-> reporter  (security key?)
- Add action to add money in navbar
- Cache trades view
- Cache trade info 
- Split commands by blueprint
- Add graph to documentation how system works
- add tests for model query
- enable pytest auto
- Add scroll to tables on views

Small tasks:

- Verify how money field is presented on navbar for: large numbers, negative numbers
- remove dev commands on deploy

## Contact

Created by <b>Marek Chałabis</b> 

email: chalabismarek@gmail.com
