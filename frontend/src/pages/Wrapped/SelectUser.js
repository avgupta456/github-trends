/* eslint-disable jsx-a11y/media-has-caption */
import React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import { BsInfoCircle } from 'react-icons/bs';
import { FaGithub as GithubIcon, FaCheck as CheckIcon } from 'react-icons/fa';

import { Button, Preview } from '../../components';
import { sleep } from '../../utils';
import wrapped1 from '../../assets/wrapped1.png';
import wrapped2 from '../../assets/wrapped2.png';
import wrapped3 from '../../assets/wrapped3.png';

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
      <div className="w-full h-full pt-16 pb-8 bg-blue-500 flex flex-wrap items-center">
        <div className="w-full lg:w-1/2 xl:w-2/5 p-8 flex flex-col items-center">
          <h1 className="text-2xl md:text-3xl lg:text-4xl font-medium mb-8 flex flex-col items-center">
            Reflect on your year
            <div>
              with <strong>GitHub Wrapped</strong>
            </div>
          </h1>
          <div className="p-8 rounded-lg bg-gray-200 shadow text-gray-800">
            <p className="text-sm lg:text-lg mb-4 flex items-center">
              <strong>Step 1</strong>: Star the GitHub Repository{' '}
              <BsInfoCircle className="h-4 w-4 ml-2 text-gray-500 hover:text-gray-800 cursor-pointer" />
            </p>
            <div className="w-full flex flex-col items-center">
              <a
                href="https://www.github.com/avgupta456/github-trends"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button className="bg-black text-white flex items-center">
                  Star on
                  <GithubIcon className="ml-1.5 w-5 h-5" />
                </Button>
              </a>
            </div>
            <p className="text-sm lg:text-lg mt-8 mb-4">
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
        <div className="w-full lg:w-1/2 xl:w-3/5 p-8 flex flex-col items-center">
          <div className="w-full xl:w-4/5 2xl:w-3/4 3xl:w-1/2 mx-auto">
            <Preview
              pages={[wrapped1, wrapped2, wrapped3]}
              details={[
                'Detailed metrics and insightful charts',
                'Lines of code metrics (by langs and repos)',
                'Over a dozen stats to reflect on your year',
              ]}
              showArrows={false}
            />
          </div>
        </div>
      </div>
      <div className="bg-gray-200 text-gray-700 w-full flex flex-col justify-center items-center pt-16">
        <h1 className="text-4xl font-medium mb-4">GitHub Trends</h1>
        <h2 className="w-3/4 text-center text-sm lg:text-lg">
          GitHub Trends dives deep into the GitHub API to bring you insightful
          metrics and shareable visualizations. We access individual commits,
          enabling a range of metrics to be displayed.
        </h2>
        <div className="w-4/5 mx-auto py-8 flex flex-wrap items-center justify-center">
          {[
            {
              header: 'Measures Contribs',
              text: 'Calculates your stats on a per-contribution level, allowing for deeper insights',
            },
            {
              header: 'LOC Insights',
              text: 'See aggregate stats on lines of code (LOC) written across all contributions',
            },
            {
              header: 'Language Breakdowns',
              text: 'Showcase your favorite languages with LOC language breakdowns',
            },
            {
              header: 'Private Mode',
              text: 'Use a PAT to avoid rate limiting and include private contributions',
            },
            {
              header: 'Exciting Visualizations',
              text: 'Visualize your contributions with bar graphs, pie charts, and more',
            },
            {
              header: 'Shareable Stats',
              text: 'Easily add your cards to your GitHub and share them online',
            },
          ].map((item, index) => (
            // eslint-disable-next-line react/no-array-index-key
            <div className="flex w-full md:w-1/2 lg:w-1/3 p-4" key={index}>
              <div className="w-4 h-4 mt-1 mr-2">
                <CheckIcon className="w-full h-full text-green-600" />
              </div>
              <div className="w-4/5 flex flex-col justify-top">
                <p className="text-xl mb-1 font-medium">{item.header}</p>
                <p>{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SelectUserScreen;
