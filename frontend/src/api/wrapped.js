/* eslint-disable no-return-await */

import axios from 'axios';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = `${BACKEND_URL}/wrapped`;

const getValidUser = async (userId) => {
  try {
    const fullUrl = `${URL_PREFIX}/valid/${userId}`;
    const result = await axios.get(fullUrl);
    return result.data.data;
  } catch (error) {
    return null;
  }
};

const getWrapped = async (userId, year) => {
  try {
    const fullUrl = `${URL_PREFIX}/${userId}?year=${year}`;
    const result = await axios.get(fullUrl);
    return result.data.data;
  } catch (error) {
    return null;
  }
};

export { getWrapped, getValidUser };
