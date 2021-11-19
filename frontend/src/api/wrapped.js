/* eslint-disable no-return-await */

import axios from 'axios';

import { SUBSCRIBER_URL } from '../constants';

const URL_PREFIX = `${SUBSCRIBER_URL}/wrapped`;

const getWrapped = async (userId, year) => {
  try {
    const fullUrl = `${URL_PREFIX}/${userId}?year=${year}`;
    console.log(fullUrl);
    const result = await axios.get(fullUrl);
    console.log(result.data.time);
    return result.data.data;
  } catch (error) {
    return null;
  }
};

export { getWrapped };
