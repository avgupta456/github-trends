import React, { useState, useEffect } from 'react';

import { useHistory } from 'react-router-dom';

import { Button } from '../../components';
import { sleep } from '../../utils';

const SelectUserScreen = () => {
  const [userName, setUserName] = useState('');

  const history = useHistory();

  let userNameInput;

  useEffect(() => {
    userNameInput.focus();
  }, [userNameInput]);

  const handleSubmit = async () => {
    await sleep(100);
    history.push(`/wrapped/${userName}`);
  };

  return (
    <div className="h-full container py-16">
      <div className="h-full w-1/3 mx-auto">
        <div className="h-full w-full bg-gray-200 rounded-xl p-8 shadow">
          <h1 className="text-2xl font-bold text-gray-800 text-center mb-4">
            GitHub Wrapped
          </h1>
          <p className="text-center text-sm text-gray-600">
            Reflect on your past year of coding growth. Enter your GitHub
            username to see interesting statistics and insights about your
            coding contributions!
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
                onKeyPress={async (e) => {
                  if (e.key === 'Enter') {
                    handleSubmit();
                  }
                }}
              />
              <Button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white"
                onClick={handleSubmit}
              >
                Go
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SelectUserScreen;
