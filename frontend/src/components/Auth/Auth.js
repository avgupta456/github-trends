import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

import { Redirect } from 'react-router-dom';

// import GithubIcon from 'mdi-react/GithubIcon';

// import { CLIENT_ID, REDIRECT_URI } from '../../constants';

const CLIENT_ID = '';
const REDIRECT_URI = '';

const LoginScreen = () => {
  const [data, setData] = useState({ errorMessage: '', isLoading: false });

  const isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const userId = useSelector((state) => state.user.userId);

  useEffect(() => {
    // After requesting Github access, Github redirects back to your app with a code parameter
    const url = window.location.href;
    const hasCode = url.includes('?code=');

    // If Github API returns the code parameter
    if (hasCode) {
      const newUrl = url.split('?code=');
      window.history.pushState({}, null, newUrl[0]);
      setData({ ...data, isLoading: true });

      const requestData = {
        code: newUrl[1],
      };

      console.log(requestData);

      /*
      const { proxyUrl } = state;

      // Use code parameter and other parameters to make POST request to proxy_server
      fetch(proxyUrl, {
        method: 'POST',
        body: JSON.stringify(requestData),
      })
        .then((response) => response.json())
        .then((responseData) => {
          dispatch({
            type: 'LOGIN',
            payload: { user: responseData, isLoggedIn: true },
          });
        })
        .catch((error) => {
          console.error(error);
          setData({
            isLoading: false,
            errorMessage: 'Sorry! Login failed',
          });
        });
      */
    }
  }, [isLoggedIn, userId, data]);

  if (isLoggedIn) {
    return <Redirect to="/" />;
  }

  return (
    <section className="container">
      <div>
        <h1>Welcome</h1>
        <span>Super amazing app</span>
        <span>{data.errorMessage}</span>
        <div className="login-container">
          {data.isLoading ? (
            <div className="loader-container">
              <div className="loader" />
            </div>
          ) : (
            <a
              className="login-link"
              href={`https://github.com/login/oauth/authorize?scope=user&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`}
              onClick={() => {
                setData({ ...data, errorMessage: '' });
              }}
            >
              {/* <GithubIcon /> */}
              <span>Login with GitHub</span>
            </a>
          )}
        </div>
      </div>
    </section>
  );
};

export default LoginScreen;
