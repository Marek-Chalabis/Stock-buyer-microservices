# AUM server
> Microservice responsible for splitting trade shares.

## Table of contents

- [General info](#general-info)
- [Setup](#setup) 
- [Tests](#tests)
- [Code format](#code-format)
- [Technologies](#technologies)
- [Contact](#contact)

## General info
Creates a random number of accounts with random percent splits between 
them that sum to 100%. 

Sends this data to the controller in intervals.

## Setup

1 Install Docker

2 Adjust environment variables in [.env](config/environment_variables/.env)

3 Change USER_ID arg in [docker-compose.yaml](docker-compose.yaml) 
if your local UID is different then 1000, this will fix local file permissions.

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
- Celery
- [Python packages](backend/pyproject.toml)


## Contact

Created by <b>Marek Chałabis</b> email: chalabismarek@gmail.com
