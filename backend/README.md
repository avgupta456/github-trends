# Backend

## Installation

```
poetry install
poetry run pre-commit install
```

## Run Locally

Navigate to localhost:8000

```
yarn start
```

## Test with Code Coverage

```
yarn test
```

View coverage with GitHub badge or on coveralls.io

## Build

If a new requirement has been added, make sure to update the requirements.txt

```
yarn set-reqs
```

Then, just commit on the main branch (Google Cloud Run takes care of the rest)

## Adding a Secret

Update cloudbuild.yaml, .env, .env-template, and GCP Cloud Run Trigger Substitution Variables.
