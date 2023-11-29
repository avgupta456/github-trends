import React from 'react';
import { useSelector } from 'react-redux';

import { FaGithub as GithubIcon } from 'react-icons/fa';

import { Button } from '../../components';
import {
  GITHUB_PUBLIC_AUTH_URL,
  GITHUB_PRIVATE_AUTH_URL,
} from '../../constants';
import { classnames } from '../../utils';

import mockup from '../../assets/mockup.png';

const SignUpScreen = () => {
  // eslint-disable-next-line no-unused-vars
  const userId = useSelector((state) => state.user.userId);

  return (
    <div className="h-full flex flex-wrap">
      <div className="hidden lg:block lg:w-3/5 lg:p-8 lg:my-auto">
        <div className="w-4/5 mx-auto">
          <img src={mockup} alt="preview" />
        </div>
      </div>
      <div className="w-full h-full lg:w-2/5 flex lg:flex-col lg:p-8">
        <div
          className={classnames(
            'bg-gray-100 rounded-sm w-full h-full m-auto p-8 shadow',
            'lg:w-80 lg:h-auto',
          )}
        >
          <h3 className="text-3xl font-semibold text-gray-900 mb-12 text-center">
            Sign up for <br />
            GitHub Trends
          </h3>
          <div>
            <a href={GITHUB_PUBLIC_AUTH_URL} className="flex justify-center">
              <Button className="h-12 flex justify-center items-center text-white bg-blue-500 hover:bg-blue-600">
                <GithubIcon className="w-4 h-4" />
                <span className="ml-2 xl:text-lg">GitHub Public Access</span>
              </Button>
            </a>
            <div className="mt-4" />
            <a href={GITHUB_PRIVATE_AUTH_URL} className="flex justify-center">
              <Button className="h-12 flex justify-center items-center text-black border border-black bg-white hover:bg-gray-100">
                <GithubIcon className="w-4 h-4" />
                <span className="ml-2 xl:text-lg">GitHub Private Access</span>
              </Button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUpScreen;
