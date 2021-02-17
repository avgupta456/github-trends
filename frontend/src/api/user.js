import axios from 'axios';

const URL_PREFIX = 'http://localhost:8000/';

const getUserData = async (user) => {
  try {
    const fullUrl = `${URL_PREFIX}user/${user}`;
    const result = await axios.get(fullUrl);
    return result.data.data;
  } catch (error) {
    return [];
  }
};

export { getUserData };
