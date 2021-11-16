import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = `${BACKEND_URL}/wrapped`;

const getWrapped = async (userId, year) => {
  try {
    const fullUrl = `${URL_PREFIX}/${userId}?year=${year}`;
    const result = await axios.get(fullUrl);
    return result.data.data;
  } catch (error) {
    console.error(error);
    return '';
  }
};

export { getWrapped };
