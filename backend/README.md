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

```
poetry run uvicorn main:app --reload
```
