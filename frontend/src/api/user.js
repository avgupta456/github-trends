import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = `${BACKEND_URL}/auth`;

const authenticate = async (code, privateAccess) => {
  try {
    const fullUrl = `${URL_PREFIX}/login/${code}?private_access=${privateAccess}`;
    const result = await axios.post(fullUrl);
    return result.data.data;
  } catch (error) {
    console.error(error);
    return '';
  }
};

export { authenticate };
