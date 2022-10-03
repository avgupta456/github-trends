// eslint-disable-next-line no-unused-vars
import React, { useEffect } from 'react';
import { BACKEND_URL } from '../../constants';

const RedirectScreen = () => {
  useEffect(() => {
    async function redirectCode() {
      // Take any query parameters and pass to redirect
      const url = window.location.href;
      const hasCode = url.includes('user/redirect');

      // If Github API returns the code parameter
      if (hasCode) {
        const newUrl = url.split('user/redirect');
        window.location.replace(`${BACKEND_URL}/auth/redirect${newUrl[1]}`);
      }
    }

    redirectCode();
  }, []);

  return null;
};

export default RedirectScreen;
