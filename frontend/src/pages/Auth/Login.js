import React from 'react';
import { useSelector } from 'react-redux';

import GithubIcon from 'mdi-react/GithubIcon';

import { Button } from '../../components';
import { GITHUB_AUTH_URL } from '../../constants';

const LoginScreen = () => {
  // const isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const userId = useSelector((state) => state.user.userId);

  console.log(userId);

  return (
    <div className="h-full py-8">
      <div className="h-full flex justify-center items-center">
        <div className="h-auto w-72 bg-gray-100 border-2 border-gray-300 rounded p-4">
          <h3 className="text-xl font-semibold text-gray-900">
            Login with GitHub!
          </h3>
          <div className="mt-2 text-xs text-gray-600">
            Authenticate with your GitHub account to access your statistics. You
            can optionally give read access to private repositories.
          </div>
          <div className="mt-4 flex justify-center">
            <a href={GITHUB_AUTH_URL} className="inline-flex">
              <Button className="text-white bg-blue-500 hover:bg-blue-600">
                <span className="mr-2">Login with GitHub</span>
                <GithubIcon />
              </Button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginScreen;
