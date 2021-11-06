import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

import { BACKEND_URL } from '../constants';

const URL_PREFIX = BACKEND_URL;

const setUserKey = async (code) => {
  try {
    const key = uuidv4();
    const fullUrl = `${URL_PREFIX}/auth/web/set_user_key/${code}/${key}`;
    await axios.post(fullUrl);
    return key;
  } catch (error) {
    console.error(error);
    return '';
  }
};

const authenticate = async (code, privateAccess) => {
  try {
    const fullUrl = `${URL_PREFIX}/auth/web/login/${code}?private_access=${privateAccess}`;
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

const deleteAccount = async (userId, userKey) => {
  try {
    const fullUrl = `${URL_PREFIX}/auth/web/delete/${userId}?user_key=${userKey}`;
    const result = await axios.get(fullUrl);
    return result.data; // no decorator
  } catch (error) {
    console.error(error);
    return '';
  }
};

export { setUserKey, authenticate, getUserMetadata, deleteAccount };
