export const USE_LOGGER = true;

export const CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
export const REDIRECT_URI = 'http://localhost:3000/user';
export const GITHUB_AUTH_URL = `https://github.com/login/oauth/authorize?scope=user,repo&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;
