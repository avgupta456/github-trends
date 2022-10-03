import React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

import { Button } from '../../components';
import { sleep } from '../../utils';

const SelectUserScreen = () => {
  const [userName, setUserName] = useState('');

  const navigate = useNavigate();

  let userNameInput;

  useEffect(() => {
    userNameInput.focus();
  }, [userNameInput]);

  const handleSubmit = async () => {
    await sleep(100);
    navigate(`/wrapped/${userName}`);
  };

  return (
    <div className="h-full w-full container mx-auto md:py-16">
      <div className="h-full w-full md:w-1/2 xl:w-1/3 mx-auto flex justify-center items-center">
        <div className="h-full md:h-auto w-full bg-gray-50 p-8 shadow">
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
