/* eslint-disable react/button-has-type */
import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import { Button } from '../../components';
import { classnames } from '../../utils';

import mockup from '../../assets/mockup.png';

const LandingScreen = () => {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  return (
    <section>
      <div className="bg-blue-500 text-gray-100 w-full flex flex-wrap py-16 px-4">
        <div className="w-1/2 flex flex-col justify-center p-4">
          <div className="w-full text-center text-5xl font-bold mb-6">
            Discover and share code contribution insights
          </div>
          <div className="w-full text-center text-lg mb-2">
            GitHub Trends dives deep into the GitHub API to bring you insightful
            metrics on your contributions, broken by repository and language.
          </div>
          <div className="w-full flex flex-wrap justify-center">
            <Link to={isAuthenticated ? '/user' : '/signup'} className="w-auto">
              <Button
                className={classnames(
                  'my-4 mr-4 w-auto justify-center bg-gray-700 hover:bg-gray-800',
                  'text-xl',
                )}
              >
                {isAuthenticated ? 'Visit Dashboard' : 'Get Started'}
              </Button>
            </Link>
            <a
              href="https://www.github.com/avgupta456/github-trends"
              target="_blank"
              rel="noopener noreferrer"
              className="w-auto"
            >
              <Button
                className={classnames(
                  'my-4 w-auto flex justify-center items-center bg-gray-100 hover:bg-gray-200',
                  'text-gray-700 text-xl',
                )}
              >
                Star on
                <GithubIcon className="ml-2 w-6 h-6" />
              </Button>
            </a>
          </div>
        </div>
        <div className="w-1/2 flex items-center p-4">
          <img src={mockup} alt="preview" />
        </div>
      </div>
      <div className="bg-gray-100 text-gray-700 w-full flex flex-wrap py-16 px-4">
        <div>Test</div>
      </div>
    </section>
  );
};

export default LandingScreen;
