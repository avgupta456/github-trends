/* eslint-disable react/button-has-type */
import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import { Button, Preview } from '../../components';
import { classnames } from '../../utils';

const LandingScreen = () => {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  return (
    <section className="bg-gray-50 text-gray-600 body-font lg:h-screen 2xl:py-16">
      <div className="container mx-auto my-auto flex flex-col items-center px-4 md:px-16 xl:px-8 xl:flex-row">
        <div
          className={classnames(
            'bg-gray-50 w-full py-16 flex flex-col items-center text-center',
            'xl:w-1/2 xl:mb-16 xl:items-start xl:text-left xl:flex-grow',
          )}
        >
          <h1 className="title-font text-3xl mb-6 font-medium text-gray-900 sm:text-4xl xl:text-5xl 2xl:text-6xl">
            GitHub Trends
          </h1>
          <div className="mb-2 leading-relaxed lg:text-lg xl:text-xl 2xl:text-2xl">
            Discover and display statistics about your code contributions!
            <p className="h-4 xl:h-2" />
            Generate insights on lines written by language and repository.
          </div>
          <div className="w-full xl:w-auto flex flex-wrap justify-center">
            <Link
              to={isAuthenticated ? '/user' : '/signup'}
              className="w-full xl:w-auto"
            >
              <Button
                className={classnames(
                  'my-4 w-full justify-center text-white bg-blue-500 hover:bg-blue-600 xl:w-auto xl:mr-4',
                  'lg:text-lg xl:text-xl 2xl:text-2xl',
                )}
              >
                {isAuthenticated ? 'Visit Dashboard' : 'Get Started'}
              </Button>
            </Link>
            <a
              href="https://www.github.com/avgupta456/github-trends"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full xl:w-auto"
            >
              <Button
                className={classnames(
                  'my-4 w-full flex justify-center items-center text-gray-700 bg-white hover:bg-gray-100 border border-gray-700 xl:w-auto',
                  'lg:text-lg xl:text-xl 2xl:text-2xl',
                )}
              >
                Star on
                <GithubIcon className="ml-2 w-5 h-5 2xl:w-7 2xl:h-7" />
              </Button>
            </a>
          </div>
        </div>
        <div className="md:block md:w-full xl:w-1/2 xl:px-12">
          <Preview />
        </div>
      </div>
    </section>
  );
};

export default LandingScreen;
