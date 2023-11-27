# GitHub Trends

If you are interested in contributing to GitHub Trends, take a look through the codebase and at the open issues. Follow the guide below to set up your local environment, and contact Abhijit Gupta at `avgupta456@gmail.com` if you have any questions or need additional permissions. Thank you in advance for contributing!

## Local Development

First, copy `backend/.env-template` into `backend/.env` and fill in the missing variables. Similarly, copy `frontend/.env-template` into `frontend/.env` and fill in the missing variables. Create a Google Cloud Platform service account and include the key in `backend/gcloud_key.json`. Then run:

With Python3.11, install the dependencies from `backend/requirements.txt` and run `yarn start`.

With Node16 and Yarn, install the dependencies from `frontend/package.json` and run on a separate terminal window `yarn start-trends`.

## Testing

Create a pull request and let GitHub Actions run. Alternatively, explore `.github/backend.yaml` and `.github/frontend.yaml` to run tests locally. Backend coverage must increase for PRs to be merged.
