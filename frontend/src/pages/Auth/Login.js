import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';

import GithubIcon from 'mdi-react/GithubIcon';

import { Button } from '../../components';
import previewImage from '../../assets/preview.png';
import { GITHUB_PUBLIC_AUTH_URL } from '../../constants';

const LoginScreen = () => {
  // eslint-disable-next-line no-unused-vars
  const userId = useSelector((state) => state.user.userId);

  return (
    <div className="h-full py-8 flex flex-wrap">
      <div className="lg:w-2/3 w-1/2">
        <img className="w-1/2 mx-auto" src={previewImage} alt="preview" />
      </div>
      <div className="lg:w-1/3 w-1/2 flex flex-col justify-center">
        <div className="bg-gray-100 rounded-lg mr-8 p-8">
          <h3 className="w-60 text-4xl font-semibold text-gray-900 mb-12">
            Log in to GitHub Trends
          </h3>
          <a href={GITHUB_PUBLIC_AUTH_URL} className="w-full">
            <Button className="w-full h-12 flex justify-center items-center text-white bg-blue-500 hover:bg-blue-600">
              <GithubIcon className="w-4 h-4" />
              <span className="ml-2">Continue with GitHub</span>
            </Button>
          </a>
          <h2 className="w-60 text-m text-gray-900 mt-8">
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
