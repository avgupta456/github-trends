import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

// import { Redirect } from 'react-router-dom';

// import GithubIcon from 'mdi-react/GithubIcon';

import { getAccessToken } from '../../api';
import {
  login as _login,
  logout as _logout,
} from '../../redux/actions/userActions';
import { CLIENT_ID, REDIRECT_URI } from '../../constants';

const GitHubAuthURL = `https://github.com/login/oauth/authorize?scope=user,repo&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`;

const LoginScreen = () => {
  const [isLoading, setIsLoading] = useState(false);

  // const isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const userId = useSelector((state) => state.user.userId);

  const dispatch = useDispatch();

  const login = (newUserId) => dispatch(_login(newUserId));
  const logout = () => dispatch(_logout());

  console.log(userId);

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

  return (
    <div>
      <h1>{`Welcome ${userId}!`}</h1>
      <span>Super amazing app</span>
      <div>
        {!isLoading && (
          <div>
            <button type="button">
              <a href={GitHubAuthURL}>
                {/* <GithubIcon /> */}
                <span>Login with GitHub</span>
              </a>
            </button>
            <button type="button" onClick={logout}>
              <span>Logout</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoginScreen;
