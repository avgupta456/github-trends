// eslint-disable-next-line no-unused-vars
import React from 'react';
import { BACKEND_URL } from '../../constants';

const RedirectScreen = () => {
  window.location.replace(`${BACKEND_URL}/auth/success`);
  return null;
};

export default RedirectScreen;
