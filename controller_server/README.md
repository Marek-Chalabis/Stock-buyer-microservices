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
- Redis
- FastAPI
- [Python packages](backend/pyproject.toml)


## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com
