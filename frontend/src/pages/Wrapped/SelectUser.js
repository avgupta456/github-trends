/* eslint-disable no-alert */
/* eslint-disable no-unused-vars */

import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import { useNavigate, Link } from 'react-router-dom';
import { ClipLoader } from 'react-spinners';
import { BsInfoCircle } from 'react-icons/bs';
import { FaGithub as GithubIcon, FaCheck as CheckIcon } from 'react-icons/fa';

import { getValidUser } from '../../api/wrapped';
import { Button, Preview } from '../../components';
import { classnames, sleep } from '../../utils';
import wrapped1 from '../../assets/wrapped1.png';
import wrapped2 from '../../assets/wrapped2.png';
import wrapped3 from '../../assets/wrapped3.png';

const SelectUserScreen = () => {
  const userId = useSelector((state) => state.user.userId || '');

  const [userName, setUserName] = useState(userId);

  const navigate = useNavigate();

  let userNameInput;

  useEffect(() => {
    userNameInput.focus();
  }, [userNameInput]);

  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    const validUser = await getValidUser(userName);
    if (validUser === 'Valid user') {
      await sleep(100);
      navigate(`/wrapped/${userName}`);
    } else if (validUser === 'GitHub user not found') {
      setError('GitHub user not found. Check your spelling and try again.');
    } else if (validUser === 'Repo not starred') {
      setError(
        'This user has not starred the GitHub Trends repository. Please star the repo and try again.',
      );
    }
    setIsLoading(false);
  };

  return (
    <div className="w-full -mt-16 text-white">
      <div className="w-full h-full bg-blue-500 pt-24 pb-16">
        <div className="w-full h-full flex flex-wrap items-center container mx-auto">
          <div className="w-full lg:w-1/2 xl:w-2/5 flex flex-col items-center">
            <h1 className="text-xl md:text-xl lg:text-3xl font-medium mb-8 flex flex-col items-center">
              Reflect on your year
              <div>
                with <strong>GitHub Wrapped</strong>
              </div>
            </h1>
            <div className="p-6 w-80 lg:w-96 rounded-lg bg-gray-200 shadow text-gray-800">
              <div className="text-sm lg:text-lg mb-4 flex items-center">
                <p>
                  <strong>Step 1</strong>: Star the GitHub Repository.{' '}
                </p>
                <div
                  className="tooltip"
                  data-tip="This helps prevent spam requests and protect user privacy. Feel free to unstar after."
                >
                  <BsInfoCircle className="h-4 w-4 ml-2 text-gray-500 hover:text-gray-800 cursor-pointer" />
                </div>
              </div>
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
                  className={classnames(
                    'bg-white text-gray-700 w-full input input-bordered rounded-sm',
                    error && 'input-error',
                  )}
                  defaultValue={userName}
                  onChange={(e) => {
                    setUserName(e.target.value);
                    setError('');
                  }}
                  onKeyPress={async (e) => {
                    if (e.key === 'Enter') {
                      handleSubmit();
                    }
                  }}
                />
                <Button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-700 text-white flex items-center"
                  onClick={handleSubmit}
                >
                  {isLoading ? (
                    <ClipLoader size={22} color="#fff" speedMultiplier={0.5} />
                  ) : (
                    'Go'
                  )}
                </Button>
              </div>
              {error ? (
                <div className="text-red-500 text-sm mt-2">
                  <strong>Error:</strong> {error}
                </div>
              ) : (
                <div className="text-sm mt-2 py-5" />
              )}
            </div>
          </div>
          <div className="w-full lg:w-1/2 xl:w-3/5 p-8 flex flex-col items-center">
            <div className="w-full xl:w-4/5 2xl:w-3/4 mx-auto">
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
      </div>
      <div className="bg-white text-gray-700 w-full py-16">
        <div className="w-full container mx-auto flex flex-col items-center">
          <h1 className="text-4xl font-medium mb-4">See some examples</h1>
          <div className="w-full flex flex-wrap justify-center items-center px-4">
            {[
              {
                name: 'Linus Torvalds',
                username: 'torvalds',
                url: 'https://avatars.githubusercontent.com/u/1024025?v=4',
                blurb: 'Creator of Linux',
              },
              {
                name: 'Evan You',
                username: 'yyx990803',
                url: 'https://avatars.githubusercontent.com/u/499550?v=4',
                blurb: 'Creator of Vue',
              },
              {
                name: 'shadcn',
                username: 'shadcn',
                url: 'https://avatars.githubusercontent.com/u/124599?v=4',
                blurb: 'Vercel, shadcn/ui',
              },
              {
                name: 'Sindre Sorhus',
                username: 'sindresorhus',
                url: 'https://avatars.githubusercontent.com/u/170270?v=4',
                blurb: 'Open-sourcer',
              },
            ].map((user) => (
              <div className="w-full md:w-1/2 lg:w-1/4 p-4" key={user.username}>
                <Link to={`/wrapped/${user.username}`}>
                  <div className="w-full rounded bg-gray-50 hover:bg-gray-100 shadow p-4 flex">
                    <img
                      src={user.url}
                      alt={user.username}
                      className="w-24 h-24 rounded-full mr-4 my-auto"
                    />
                    <div className="w-full flex flex-col items-center">
                      <strong className="w-full text-center">
                        {user.name}
                      </strong>
                      <p className="w-full text-center">{user.blurb}</p>
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="bg-gray-200 text-gray-800 w-full pt-16">
        <div className="w-full container mx-auto flex flex-col items-center justify-center">
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
    </div>
  );
};

export default SelectUserScreen;
