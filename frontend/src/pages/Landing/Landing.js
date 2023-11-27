/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { FaGithub as GithubIcon, FaCheck as CheckIcon } from 'react-icons/fa';

import { Button, Preview } from '../../components';

import mockup from '../../assets/mockup.png';
import wrapped from '../../assets/wrapped1.png';
import avgupta456Langs from '../../assets/avgupta456_langs.png';
import tiangoloRepos from '../../assets/tiangolo_repos.png';
import reininkRepos from '../../assets/reinink_repos.png';
import dhermesLangs from '../../assets/dhermes_langs.png';
import { WRAPPED_URL } from '../../constants';

function LandingScreen() {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  return (
    <section>
      <div className="min-h-screen bg-blue-500 text-gray-100 w-full flex flex-wrap -mt-8 py-16 px-4">
        <div className="w-full xl:w-1/2 flex flex-col justify-center p-4">
          <div className="w-full 3xl:w-2/3 mx-auto text-center text-3xl md:text-5xl 3xl:text-6xl font-bold mb-6">
            Discover and share code contribution insights
          </div>
          <div className="w-full 3xl:w-2/3 mx-auto text-center md:text-lg 3xl:text-2xl mb-2">
            GitHub Trends dives deep into the GitHub API to bring you insightful
            metrics on your contributions, broken by repository and language.
          </div>
          <div className="w-full flex flex-wrap justify-center">
            <Link to={isAuthenticated ? '/user' : '/signup'} className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center bg-gray-700 hover:bg-gray-800 text-xl 3xl:text-2xl">
                {isAuthenticated ? 'Visit Dashboard' : 'Get Started'}
              </Button>
            </Link>
            <a
              href="https://www.github.com/avgupta456/github-trends"
              target="_blank"
              rel="noopener noreferrer"
              className="w-auto"
            >
              <Button className="my-4 w-auto flex justify-center items-center bg-gray-100 hover:bg-gray-200 text-gray-700 text-xl 3xl:text-2xl">
                Star on
                <GithubIcon className="ml-2 w-6 h-6" />
              </Button>
            </a>
          </div>
        </div>
        <div className="hidden md:flex w-3/4 xl:w-1/2 mx-auto items-center p-4">
          <img src={mockup} alt="preview" />
        </div>
      </div>
      <div className="bg-gray-200 text-gray-700 w-full flex flex-wrap items-center py-4 px-4">
        <div className="w-full lg:w-1/2 p-8 flex justify-center">
          <Preview
            pages={[avgupta456Langs, tiangoloRepos, reininkRepos, dhermesLangs]}
            details={[
              'Abhijit Gupta (avgupta456): GitHub Trends',
              'Sebastián Ramírez (tiangolo): FastAPI',
              'Jonathan Reinink (reinink): TailwindCSS',
              'Danny Hermes (dhermes): Google PubSub',
            ]}
            showArrows
          />
        </div>
        <div className="w-full lg:w-1/2 3xl:w-1/3 mx-auto p-8 flex flex-col">
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
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-gray-700 hover:bg-gray-800">
                {isAuthenticated ? 'Visit Dashboard' : 'Try the Demo'}
              </Button>
            </Link>
            {!isAuthenticated && (
              <Link to="/signup" className="w-auto">
                <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-blue-500 hover:bg-blue-600">
                  Get Started
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>
      <div className="text-gray-700 w-full flex flex-wrap items-center py-4 px-4">
        <div className="w-full lg:w-1/2 3xl:w-1/3 mx-auto p-8 flex flex-col">
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
          <div>
            <Link to={`${WRAPPED_URL}/avgupta456`} className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-gray-700 hover:bg-gray-800">
                Example
              </Button>
            </Link>
            <Link
              to={isAuthenticated ? `${WRAPPED_URL}/${userId}` : WRAPPED_URL}
              className="w-auto"
            >
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-blue-500 hover:bg-blue-600">
                Get your Wrapped
              </Button>
            </Link>
          </div>
        </div>
        <div className="w-full lg:w-1/2 p-8">
          <div className="flex justify-center">
            <img src={wrapped} alt="preview" />
          </div>
        </div>
      </div>
      <div className="bg-gray-200 text-gray-700 w-full flex flex-col justify-center items-center pt-16 py-4 px-4">
        <h1 className="text-4xl font-medium mb-4">GitHub Trends</h1>
        <h2 className="w-2/3 text-center text-lg">
          GitHub Trends dives deep into the GitHub API to bring you insightful
          metrics and visualizations. We access individual commits to compute
          accurate and granular statistics.
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
      {!isAuthenticated && (
        <div className="text-gray-700 w-full flex flex-col justify-center items-center py-16 px-4">
          <p className="text-3xl font-medium">Ready to get started?</p>
          <p className="text-3xl font-medium">Create an account today.</p>
          <div className="mt-2">
            <Link to="/demo" className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-gray-700 hover:bg-gray-800">
                Try Demo
              </Button>
            </Link>
            <Link to="/signup" className="w-auto">
              <Button className="my-4 mr-4 w-auto justify-center text-white text-xl 3xl:text-2xl bg-blue-500 hover:bg-blue-600">
                Sign Up
              </Button>
            </Link>
          </div>
        </div>
      )}
    </section>
  );
}

export default LandingScreen;
