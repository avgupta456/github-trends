# Backend

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

View coverage with GitHub badge or on coveralls.io

## Build

If a new requirement has been added, make sure to update the requirements.txt

```
poetry export -f requirements.txt --output requirements.txt --without-hashes # generate requirements.txt
```

Then, just commit on the main branch (Google Cloud Run takes care of the rest)

## Adding a Secret

Update cloudbuild_pub.yaml, cloudbuild_sub.yaml, .env, .env-template, and GCP Cloud Run Trigger Substitution Variables.
