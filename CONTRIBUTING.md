# GitHub Trends

## Local Development

First, copy `backend/.env-template` into `backend/.env` and fill in the missing variables. Similarly, copy `frontend/.env-template` into `frontend/.env` and fill in the missing variables. Create a Google Cloud Platform service account and include the key in `backend/gcloud_key.json`. Then run:

### Docker (recommended)

```
docker-compose up --build -d
```

### Manual

With Python3.8, install the dependencies from `backend/requirements.txt` and run on two separate terminal windows

```
poetry run uvicorn src.main_pub:app --reload --port=8000
poetry run uvicorn src.main_sub:app --reload --port=8001
```

With Node16 and Yarn, install the dependencies from `frontend/package.json` and run on a separate terminal window

```
yarn start
```

## Testing

Create a pull request and let GitHub Actions run. Alternatively, explore `.github/backend.yaml` and `.github/frontend.yaml` to run tests locally. Backend coverage must increase for PRs to be merged.

## FAQ

(In Progress)

## Action Items

1. Unblock development without secrets (guide on creating MongoDB database, GCP project, GitHub App, etc.)
2. FAQ
