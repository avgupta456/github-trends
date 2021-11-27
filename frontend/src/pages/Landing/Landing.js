/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import { Button, Preview } from '../../components';
import { classnames } from '../../utils';

import mockup from '../../assets/mockup.png';
import wrapped from '../../assets/wrapped.png';

const LandingScreen = () => {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  return (
    <section>
      <div className="bg-blue-500 text-gray-100 w-full flex flex-wrap py-24 px-4">
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
      <div className="bg-gray-200 text-gray-700 w-full flex flex-wrap items-center py-4 px-4">
        <div className="w-1/2 p-8 flex justify-center">
          <Preview />
        </div>
        <div className="w-1/2 p-8 flex flex-col">
          <h1 className="text-4xl text-gray-900 font-medium mb-12">
            Display your GitHub stats
            <div>with embeddable cards</div>
          </h1>
          <p className="text-lg font-bold">1. Comprehensive</p>
          <p>
            GitHub Trends counts each individual commit, across all your
            open-source contributions. We surface line of code metrics by
            repository and languages.
          </p>
          <br />
          <p className="text-lg font-bold">2. Customizable</p>
          <p>
            Using the online dashboard, easily modify the time range, include
            private commits, and choose your display theme.
          </p>
          <br />
          <p className="text-lg font-bold">3. Shareable</p>
          <p>
            Share your GitHub Trends cards as a PNG on Twitter, or as a dynamic
            embeddable image on your GitHub profile or personal website.
          </p>
          <br />
          <div>
            <Link to={isAuthenticated ? '/user' : '/demo'} className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-gray-700 hover:bg-gray-800">
                {isAuthenticated ? 'Visit Dashboard' : 'Try the Demo'}
              </Button>
            </Link>
            {!isAuthenticated && (
              <Link to="/signup" className="w-auto">
                <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-blue-500 hover:bg-blue-600">
                  Get Started
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>
      <div className="text-gray-700 w-full flex flex-wrap items-center py-4 px-4">
        <div className="w-1/2 p-8 flex flex-col">
          <h1 className="text-4xl text-gray-900 font-medium mb-12">
            Reflect on your year
            <div>
              with <strong>GitHub Wrapped</strong>
            </div>
          </h1>
          <p className="text-lg font-bold">1. Detailed</p>
          <p>
            GitHub Wrapped provides a breakdown of your contributions by date,
            by date, time, repository, and language. Over 20 stats are
            displayed.
          </p>
          <br />
          <p className="text-lg font-bold">2. Visual</p>
          <p>
            Understand your coding contributions like never before with an
            interactive calendar, bar charts, pie charts, swarm graphs, and
            more.
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
          <div>
            <Link to="/wrapped/avgupta456" className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-gray-700 hover:bg-gray-800">
                Example
              </Button>
            </Link>
            <Link
              to={isAuthenticated ? `/wrapped/${userId}` : '/wrapped'}
              className="w-auto"
            >
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-blue-500 hover:bg-blue-600">
                Get your Wrapped
              </Button>
            </Link>
          </div>
        </div>
        <div className="w-1/2 p-8">
          <div className="flex justify-center">
            <img src={wrapped} alt="preview" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default LandingScreen;
