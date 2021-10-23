import React, { useEffect, useState } from 'react';

import { Link } from 'react-router-dom';

import { Button, SvgInline } from '../../components';

import { BACKEND_URL } from '../../constants';

const DemoScreen = () => {
  const [userName, setUserName] = useState('');
  const [selectedUserName, setSelectedUserName] = useState('');

  let userNameInput;

  console.log(`${BACKEND_URL}/user/svg/${selectedUserName}/repos?demo=true`);

  useEffect(() => {
    userNameInput.focus();
  }, [userNameInput]);

  return (
    <div className="h-full py-8 flex justify-center items-center">
      <div className="h-full w-1/3 pl-8">
        <div className="h-full w-full bg-gray-50 rounded-xl p-4">
          <h1 className="text-2xl font-bold text-gray-800 text-center mb-4">
            GitHub Trends Demo
          </h1>
          <p className="text-center text-sm text-gray-600">
            This is a demo of the GitHub Trends API. Enter your GitHub username
            to see statistics about your top languages and repositories from the
            past month.
          </p>
          <div className="form-control my-8">
            <p>Enter your GitHub username to get started!</p>
            <div className="flex space-x-2 mt-2">
              <input
                type="text"
                ref={(input) => {
                  userNameInput = input;
                }}
                placeholder="Enter Username"
                className="bg-white text-gray-700 w-full input input-bordered"
                onChange={(e) => setUserName(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    setSelectedUserName(userName);
                  }
                }}
              />
              <Button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white"
                onClick={() => setSelectedUserName(userName)}
              >
                Go
              </Button>
            </div>
          </div>
          <p className="text-center text-sm text-red-500">
            This demo uses a public access token that is heavily rate limited.
            For full customization, private contributions, and a personal access
            token, create an account instead!
          </p>
          <div className="flex justify-center mt-8">
            <Button className="text-white bg-blue-500 hover:bg-blue-600">
              <Link to="/signup">Create an Account</Link>
            </Button>
          </div>
        </div>
      </div>
      <div className="h-full w-2/3 px-8">
        <div className="h-full w-full bg-gray-50 rounded-xl p-4">
          <h1 className="text-2xl font-bold text-gray-800 text-center mb-4">
            {selectedUserName === ''
              ? 'Enter a Username'
              : `Example Cards for ${selectedUserName}`}
          </h1>
          <div className="w-full flex flex-wrap">
            <div className="w-1/2 p-2">
              <SvgInline
                className="w-full h-full"
                forceLoading={selectedUserName === ''}
                url={`${BACKEND_URL}/user/svg/${selectedUserName}/langs?demo=true`}
              />
            </div>
            <div className="w-1/2 p-2">
              <SvgInline
                className="w-full h-full"
                forceLoading={selectedUserName === ''}
                url={`${BACKEND_URL}/user/svg/${selectedUserName}/repos?demo=true`}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoScreen;
