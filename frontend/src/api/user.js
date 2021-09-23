import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = `${BACKEND_URL}/auth/`;

const getAccessToken = async (code) => {
  try {
    const fullUrl = `${URL_PREFIX}login/${code}`;
    const result = await axios.post(fullUrl);
    console.log(result.data.data);
    return result.data.data;
  } catch (error) {
    console.error(error);
    return '';
  }
};

export { getAccessToken };
