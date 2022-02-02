!!!WIP!!!

Monster tasks:

- Add full trades logic. Remember about:
```
co jeśli idzie fill ale nie ma już konta
co jesli nie ma akcji
kupuje na tyle na ile go stac w danym momencie
```

- Add frontend framework
Big tasks:

- Divides settings/env for prod and develop
- Add auto trade option for users, by switch on model
- Add an image for user avatar, also enable changing it
- Add migrations (alembic)
- Implement FastAPI for API side of application (FastAPI will be a main server graphql?)
- Implement Celery/redis for tasks 
- Add auto population DB with users stock fills and trades

Medium tasks:

- Allow password change
- Add script for postgresql wait on docker compose up
- Security: microservices <-> reporter  (security key?)
- Add action to add money in navbar
- Cache trades view
- Cache trade info 
- Split commands by blueprint
- Add graph to documentation how system works

Small tasks:

- Verify how money field is presented on navbar for: large numbers, negative numbers

# Controller server
> Microservice responsible for creating stock purchase order from gathered data and sending them to reporter.

## Table of contents

- [General info](#general-info)
- [API documentation](#api-documentation)
- [Setup](#setup) 
- [Tests](#tests)
- [Code format](#code-format)
- [Technologies](#technologies)
- [Contact](#contact)

## General info
The controller is keeping track of positions held by each account got from the aum server
When new fill come in it divides the stocks so that each account has an overall position 
that matches the split from aum server, then sends stock purchase order to reporter.

## API documentation
Documentation for API can found at this endpoints after running container:

- `/docs/` : Documentation endpoint 

This is only for test/showcase, remove line 23 and 24 from 
[.docker-compose.yaml](docker-compose.yaml),
this will free port 8001 on your local machine

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

docker-compose run --rm app poetry lock

docker-compose exec app python src/commands.py restart_main_db
docker exec -it reporter_app_1 /bin/bash
from app import db; db.drop_all(); db.create_all(); db.session.commit()

- FastAPI
- [Python packages](backend/pyproject.toml)


## Contact

Created by <b>Marek Chałabis</b> 

email: chalabismarek@gmail.com
