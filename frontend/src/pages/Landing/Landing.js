/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { FaGithub as GithubIcon, FaCheck as CheckIcon } from 'react-icons/fa';

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
      <div className="bg-gray-200 text-gray-700 w-full flex flex-col justify-center items-center pt-16 py-4 px-4">
        <h1 className="text-4xl font-medium mb-4">GitHub Trends</h1>
        <h2 className="w-2/3 text-center text-lg">
          GitHub Trends dives deep into the GitHub API to bring you insightful
          metrics and shareable visualizations. We access individual commits,
          enabling a range of metrics to be displayed.
        </h2>
        <div className="w-4/5 mx-auto py-8 flex flex-wrap items-center justify-center">
          {[
            {
              header: 'Measures Contribution',
              text:
                'GitHub Trends calculates your stats on a per-contribution level, allowing for deeper insights',
            },
            {
              header: 'LOC Insights',
              text:
                'See aggregate stats on lines of code (LOC) written across all contributions',
            },
            {
              header: 'Language Breakdowns',
              text:
                'Showcase your favorite languages with LOC language breakdowns',
            },
            {
              header: 'Private Mode',
              text:
                'Use a personal access token to avoid rate limiting and include private contributions',
            },
            {
              header: 'Exciting Visualizations',
              text:
                'Visualize your contributions with bar charts, swarm plots, pie charts, and more',
            },
            {
              header: 'Shareable Stats',
              text:
                'Easily add your cards to your GitHub profile and share them on Twitter or Linkedin',
            },
          ].map((item, index) => (
            // eslint-disable-next-line react/no-array-index-key
            <div className="flex w-1/3 p-4" key={index}>
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
      {!isAuthenticated && (
        <div className="text-gray-700 w-full flex flex-col justify-center items-center py-16 px-4">
          <p className="text-3xl font-medium">Ready to get started?</p>
          <p className="text-3xl font-medium">Create an account today.</p>
          <div className="mt-2">
            <Link to="/demo" className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-gray-700 hover:bg-gray-800">
                Try Demo
              </Button>
            </Link>
            <Link to="/signup" className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl bg-blue-500 hover:bg-blue-600">
                Sign Up
              </Button>
            </Link>
          </div>
        </div>
      )}
    </section>
  );
};

export default LandingScreen;
