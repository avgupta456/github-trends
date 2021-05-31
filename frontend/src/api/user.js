import axios from 'axios';

const URL_PREFIX = 'http://localhost:8000/';

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
