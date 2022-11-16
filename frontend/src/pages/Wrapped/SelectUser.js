import React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import { BsInfoCircle } from 'react-icons/bs';

import { Button } from '../../components';
import { sleep } from '../../utils';
import wrapped from '../../assets/wrapped.png';
import loc from '../../assets/loc.png';

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
    <div className="w-full -mt-16 text-white">
      <div className="w-full h-full mt-16 bg-blue-500 flex items-center py-4 px-4">
        <div className="w-full lg:w-1/2 p-8 flex flex-col items-center justify-center">
          <h1 className="text-4xl font-medium mb-12 flex flex-col items-center">
            Reflect on your year
            <div>
              with <strong>GitHub Wrapped</strong>
            </div>
          </h1>
          <div className="p-6 rounded-lg bg-white shadow text-gray-800">
            <p className="text-lg mb-4 flex items-center">
              <strong>Step 1</strong>: Star the GitHub Repository{' '}
              <BsInfoCircle className="h-4 w-4 ml-2 text-gray-500 hover:text-gray-800 cursor-pointer" />
            </p>
            <Button className="w-auto justify-center text-white text-xl 3xl:text-2xl bg-gray-700 hover:bg-gray-800">
              Star the GitHub
            </Button>
            <p className="text-lg mt-8 mb-4">
              <strong>Step 2</strong>: Enter your GitHub username!
            </p>
            <div className="flex space-x-2 mt-2">
              <input
                type="text"
                ref={(input) => {
                  userNameInput = input;
                }}
                placeholder="Enter Username"
                className="bg-white text-gray-700 w-full input input-bordered rounded-sm"
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
        <div className="w-full lg:w-1/2 p-8 flex flex-col items-center">
          <img className="w-1/2 h-1/2" src={loc} alt="preview" />
        </div>
      </div>
      <img src={wrapped} alt="preview" />
      <div>
        <p className="text-lg font-bold">1. Detailed</p>
        <p>
          GitHub Wrapped provides a breakdown of your contributions by date, by
          date, time, repository, and language. Over 20 stats are displayed.
        </p>
        <br />
        <p className="text-lg font-bold">2. Visual</p>
        <p>
          Understand your coding contributions like never before with an
          interactive calendar, bar charts, pie charts, and more.
        </p>
        <br />
        <p className="text-lg font-bold">3. Public</p>
        <p>
          Share your GitHub Wrapped link with your friends and colleagues and
          take a look at their contributions too.{' '}
          <strong>No account required</strong>, although rate limiting may
          apply.
        </p>
        <br />
      </div>
    </div>
  );
};

export default SelectUserScreen;
