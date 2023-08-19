# fastapi-skeleton
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Branch
### develop
FastAPI skeleton to start project faster
### auth
FastAPI skeleton for authentication using jwt
### oauth2
FastAPI skeleton for oauth2 authentication using jwt
## Installation

upload image to docker for local environment
```bash
docker-compose -f docker-compose.yml up -d
```

install dependencies of this project
```bash
python3 -m pip install --upgrade pip
pip3 install poetry==1.4.0
poetry install
```

## Run

### server
```bash
poetry run task server
```

### test
```bash
poetry run task test
```

### lint
```bash
poetry run task lint
```
