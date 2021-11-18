/* eslint-disable no-return-await */

import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = `${BACKEND_URL}/wrapped`;

const getWrapped = async (userId, year, retries = 0) => {
  try {
    const fullUrl = `${URL_PREFIX}/${userId}?year=${year}`;
    const result = await axios.get(fullUrl);
    const output = result.data.data;
    if (output === null || output === undefined) {
      throw new Error('No data');
    }
    return output;
  } catch (error) {
    if (retries < 3) {
      return await getWrapped(userId, year, retries + 1);
    }
    console.error(error);
    return null;
  }
};

export { getWrapped };
