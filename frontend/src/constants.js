export const PROD = process.env.REACT_APP_PROD === 'true';

export const USE_LOGGER = true;

export const CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
export const REDIRECT_URI = PROD
  ? 'https://githubtrends.io/user'
  : 'http://localhost:3000/user';
export const GITHUB_AUTH_URL = `https://github.com/login/oauth/authorize?scope=user,repo&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;

export const BACKEND_URL = PROD
  ? 'api.githubtrends.io'
  : 'http://localhost:8000';
