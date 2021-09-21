import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import BounceLoader from 'react-spinners/BounceLoader';

import { getAccessToken } from '../../api';
import { login as _login } from '../../redux/actions/userActions';

const HomeScreen = () => {
  const [isLoading, setIsLoading] = useState(false);

  // const isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const login = (newUserId) => dispatch(_login(newUserId));

  console.log(isLoading, userId);

  useEffect(async () => {
    // After requesting Github access, Github redirects back to your app with a code parameter
    const url = window.location.href;
    const hasCode = url.includes('?code=');

    // If Github API returns the code parameter
    if (hasCode) {
      const newUrl = url.split('?code=');
      window.history.pushState({}, null, newUrl[0]);
      setIsLoading(true);
      const result = await getAccessToken(newUrl[1]);
      login(result);
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <BounceLoader color="#3B82F6" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            Please sign in to access this page
          </h1>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full py-8 flex justify-center items-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold">{`Welcome ${userId}!`}</h1>
      </div>
    </div>
  );
};

export default HomeScreen;
