import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';

import { FaGithub as GithubIcon } from 'react-icons/fa';

import { Button, Preview } from '../../components';
import { GITHUB_PUBLIC_AUTH_URL } from '../../constants';
import { classnames } from '../../utils';

const LoginScreen = () => {
  // eslint-disable-next-line no-unused-vars
  const userId = useSelector((state) => state.user.userId);

  return (
    <div className="h-full flex flex-wrap">
      <div className="hidden lg:block lg:w-1/2 lg:p-8 lg:my-auto">
        <div className="w-4/5 mx-auto">
          <Preview />
        </div>
      </div>
      <div className="w-full h-full lg:w-1/2 flex lg:flex-col">
        <div
          className={classnames(
            'bg-gray-100 rounded-sm w-full h-full m-auto p-8 shadow',
            'lg:w-96 lg:h-auto 2xl:w-1/2 2xl:h-1/2 2xl:flex 2xl:flex-col 2xl:justify-between',
          )}
        >
          <h3 className="text-3xl 2xl:text-4xl font-semibold text-gray-900 mb-12">
            Log in to GitHub Trends
          </h3>
          <a href={GITHUB_PUBLIC_AUTH_URL} className="flex justify-center">
            <Button className="h-12 flex justify-center items-center text-white bg-blue-500 hover:bg-blue-600">
              <GithubIcon className="w-4 h-4 2xl:w-6 2xl:h-6" />
              <span className="ml-2 xl:text-lg 2xl:text-xl">
                Continue with GitHub
              </span>
            </Button>
          </a>
          <h2 className="mt-8 text-gray-900 2xl:text-lg">
            {`Don't have an account? `}
            <Link to="/signup" className="text-blue-500 hover:text-blue-600">
              Sign up!
            </Link>
          </h2>
        </div>
      </div>
    </div>
  );
};

export default LoginScreen;
