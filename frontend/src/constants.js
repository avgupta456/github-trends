export const PROD = process.env.REACT_APP_PROD === 'true';

export const USE_LOGGER = true;

export const CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
export const REDIRECT_URI = PROD
  ? 'https://www.githubtrends.io/user'
  : 'http://localhost:3000/user';
export const GITHUB_PRIVATE_AUTH_URL = `https://github.com/login/oauth/authorize?scope=user,repo&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}/private`;
export const GITHUB_PUBLIC_AUTH_URL = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}/public`;

export const BACKEND_URL = PROD
  ? 'https://api.githubtrends.io'
  : 'http://localhost:8000';

export const SUBSCRIBER_URL = PROD
  ? 'https://sub-dot-github-298920.uc.r.appspot.com'
  : 'http://localhost:8001';
