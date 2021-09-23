/* eslint-disable react/button-has-type */
import React from 'react';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';

import { Button } from '../../components';

const LandingScreen = () => {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  return (
    <section className="text-gray-600 body-font">
      <div className="container mx-auto flex px-5 py-16 md:flex-row flex-col items-center">
        <div className="lg:flex-grow md:w-1/2 lg:pr-24 md:pr-16 flex flex-col md:items-start md:text-left mb-16 md:mb-0 items-center text-center">
          <h1 className="title-font sm:text-4xl text-3xl mb-4 font-medium text-gray-900">
            GitHub Trends
          </h1>
          <p className="mb-8 leading-relaxed">
            Discover and display in-depth statistics about your code
            contributions!
            <br />
            Generate insights on lines written by language, commit frequency by
            date and time, repository contribution rankings, and more.
          </p>
          <div className="flex justify-center">
            <Link to={isAuthenticated ? '/user' : '/signup'}>
              <Button className="text-white bg-blue-500 hover:bg-blue-600">
                {isAuthenticated ? 'Visit Dashboard' : 'Get Started'}
              </Button>
            </Link>
            <a
              href="https://www.github.com/avgupta456/github-trends"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button className="ml-4 text-gray-700 bg-gray-100 hover:bg-gray-200">
                Fork on GitHub
              </Button>
            </a>
          </div>
        </div>
        <div className="lg:max-w-lg lg:w-full md:w-1/2 w-5/6">
          <img
            className="object-cover object-center rounded"
            alt="hero"
            src="https://dummyimage.com/720x600"
          />
        </div>
      </div>
    </section>
  );
};

export default LandingScreen;
