## Developer Experience

I use the following tools to improve the developer experience

- VSCode for IDE
- Poetry for Dependencies
- Flake8 for Linting (get VSCode extension)
- Pylance for Type Checking (get VSCode extension)
- UnitTest for Testing
- Coverage.py for Coverage
- GitHub Actions for CI/CD

## Installation

```
poetry config virtualenvs.in-project
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
