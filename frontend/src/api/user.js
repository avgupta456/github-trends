import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = BACKEND_URL;

const authenticate = async (code, privateAccess) => {
  try {
    const fullUrl = `${URL_PREFIX}/auth/login/${code}?private_access=${privateAccess}`;
    const result = await axios.post(fullUrl);
    return result.data.data;
  } catch (error) {
    console.error(error);
    return '';
  }
};

const getUserMetadata = async (userId) => {
  try {
    const fullUrl = `${URL_PREFIX}/user/db/get/metadata/${userId}`;
    const result = await axios.get(fullUrl);
    return result.data.data;
  } catch (error) {
    console.error(error);
    return '';
  }
};

export { authenticate, getUserMetadata };
