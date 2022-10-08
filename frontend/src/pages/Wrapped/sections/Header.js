/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';

import { Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import { FaArrowLeft as LeftArrowIcon } from 'react-icons/fa';

import { Button, WrappedCard } from '../../../components';
import { GITHUB_PRIVATE_AUTH_URL } from '../../../constants';
import { sleep } from '../../../utils';

const Header = ({ userId, year, numContribs, numLines }) => {
  const currUserId = useSelector((state) => state.user.userId);
  const usePrivate = useSelector((state) => state.user.privateAccess);

  const shareText = `In ${year}, I made ${numContribs} contributions and modified ${numLines} lines of code. Check out my GitHub Wrapped and create your own at`;
  const shareUrl = `githubtrends.io/wrapped/${userId}`;

  const openInNewTab = (url) => {
    const newWindow = window.open(url, '_blank', 'noopener,noreferrer');
    if (newWindow) newWindow.opener = null;
  };

  const redirectTwitter = () => {
    const urlText = shareText.split(' ').join('%20');
    openInNewTab(
      `https://twitter.com/intent/tweet?text=${urlText}&url=${shareUrl}&hashtags=githubwrapped,githubtrends,github`,
    );
  };

  const redirectGitHub = () => {
    toast.info('Copied to Clipboard, redirecting...', {
      position: 'bottom-right',
      autoClose: 3000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: false,
      progress: undefined,
    });
    navigator.clipboard.writeText(`${shareText} ${shareUrl}`);
    sleep(3000).then(() => {
      openInNewTab(
        `https://github.com/${userId}/${userId}/edit/master/README.md`,
      );
    });
  };

  return (
    <div className="w-full h-auto flex flex-row flex-wrap">
      <ToastContainer
        position="bottom-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss={false}
        draggable={false}
        pauseOnHover={false}
      />
      <div className="w-full h-auto">
        <WrappedCard>
          <Link to="/wrapped">
            <LeftArrowIcon className="absolute h-6 w-6 text-gray-400 hover:text-gray-700" />
          </Link>
          <p className="text-xl font-semibold text-center w-full">
            {`${userId}'s`}
          </p>
          <p className="text-3xl text-center w-full">
            {`${year} GitHub Wrapped`}
          </p>
        </WrappedCard>
      </div>
      <div className="hidden md:block w-full md:w-1/2 lg:w-1/3">
        <WrappedCard className="justify-between">
          <p className="mb-4">
            Create an{' '}
            <a
              href="https://github.com/avgupta456/github-trends#faq"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 underline"
            >
              account
            </a>{' '}
            to include <strong>private commits</strong>.
          </p>
          {(userId === currUserId && usePrivate) || currUserId ? (
            <div className="w-full flex justify-center">
              <Button className="bg-gray-300 text-gray-500 cursor-not-allowed">
                {userId === currUserId
                  ? 'Private Access Enabled'
                  : 'Not your Account'}
              </Button>
            </div>
          ) : (
            <a
              href={`${GITHUB_PRIVATE_AUTH_URL}&login=${userId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex justify-center"
            >
              <Button className="text-white bg-blue-500 hover:bg-blue-600">
                {currUserId ? 'Upgrade your Account' : 'Create an Account'}
              </Button>
            </a>
          )}
        </WrappedCard>
      </div>
      <div className="hidden md:block w-full md:w-1/2 lg:w-1/3">
        <WrappedCard className="justify-between">
          <p className="mb-4">Share your GitHub Wrapped on Twitter!</p>
          <div className="w-full flex justify-center">
            <Button
              className="bg-blue-500 hover:bg-blue-600 text-white"
              onClick={redirectTwitter}
            >
              Share on Twitter
            </Button>
          </div>
        </WrappedCard>
      </div>
      <div className="hidden lg:block w-full md:w-1/2 lg:w-1/3">
        <WrappedCard className="justify-between">
          <p className="mb-4">Share your GitHub Wrapped on GitHub!</p>
          <div className="w-full flex justify-center">
            <Button
              className="bg-blue-500 hover:bg-blue-600 text-white"
              onClick={redirectGitHub}
            >
              Add to GitHub Profile
            </Button>
          </div>
        </WrappedCard>
      </div>
    </div>
  );
};

Header.propTypes = {
  userId: PropTypes.string.isRequired,
  year: PropTypes.string.isRequired,
  numContribs: PropTypes.any,
  numLines: PropTypes.any,
};

Header.defaultProps = {
  numContribs: 0,
  numLines: 0,
};

export default Header;
