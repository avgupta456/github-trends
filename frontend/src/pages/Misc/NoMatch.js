import React from 'react';

import { Link } from 'react-router-dom';

import { Button } from '../../components';

const NoMatchScreen = () => {
  return (
    <div className="h-full w-full flex flex-col justify-center items-center">
      <div className="flex">
        <div className="pr-8 text-5xl font-semibold text-blue-500">404</div>
        <div className="flex flex-col">
          <div className="pl-8 border-l-2 border-gray-200">
            <div className="text-5xl font-bold text-gray-900">
              Page not Found
            </div>
            <div className="text-lg text-gray-500 mt-2">
              Please check the URL in the address bar and try again.
            </div>
          </div>
          <Link to="/" className="ml-8 mt-8">
            <Button className="bg-blue-500 hover:bg-blue-600 text-white">
              Go to Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NoMatchScreen;
