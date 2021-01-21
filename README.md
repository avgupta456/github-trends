# GitHub Trends

[![Coverage Status](https://coveralls.io/repos/github/avgupta456/github-trends/badge.svg?t=jQQ3FK)](https://coveralls.io/github/avgupta456/github-trends)

## Installation

```
poetry install
poetry run pre-commit install
```

## Run Locally

Navigate to localhost:8000

```
poetry run uvicorn main:app --reload
```

## Test with Code Coverage

```
poetry run coverage -m unittest
poetry run coverage report
```

## Build

If a new requirement has been added, make sure to update the requirements.txt

```
poetry export -f requirements.txt --output requirements.txt --without-hashes # generate requirements.txt
```

TODO
