## Developer Experience

I use the following tools to improve the developer experience

- VSCode for IDE
- Flake8 for Linting (get VSCode extension)
- Pylance for Type Checking (get VSCode extension)
- Poetry for Dependencies

## Installation

```
poetry config virtualenvs.in-project
poetry init
```

## Run Locally

Navigate to localhost:8000

```
poetry run uvicorn main:app --reload
```

## Build

If a new requirement has been added, make sure to update the requirements.txt

```
poetry export -f requirements.txt --output requirements.txt --without-hashes # generate requirements.txt
```

TODO
