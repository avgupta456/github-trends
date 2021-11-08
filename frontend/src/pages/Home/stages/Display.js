/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { Card, Button } from '../../../components';
import { classnames, sleep } from '../../../utils';

const DisplayStage = ({ userId, themeSuffix }) => {
  const openInNewTab = (url) => {
    const newWindow = window.open(url, '_blank', 'noopener,noreferrer');
    if (newWindow) newWindow.opener = null;
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
    navigator.clipboard.writeText(
      `[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/${userId}/${themeSuffix})](https://githubtrends.io)`,
    );
    sleep(3000).then(() => {
      openInNewTab(
        `https://github.com/${userId}/${userId}/edit/master/README.md`,
      );
    });
  };

  return (
    <div className="w-full flex flex-wrap">
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
      <div className="h-auto lg:w-2/5 md:w-1/2 pr-10 p-10 rounded bg-gray-100">
        <div>
          Share your GitHub Trends card through multiple channels, including
          GitHub, Twitter, and Linkedin. Or, download the PNG and share
          anywhere!
        </div>
        <br />
        <div className="flex flex-col items-center">
          {[
            {
              title: 'Display on GitHub',
              active: true,
              onClick: redirectGitHub,
            },
            { title: 'Share on Twitter', active: false, onClick: null },
            { title: 'Share on LinkedIn', active: false, onClick: null },
            { title: 'Download PNG', active: false, onClick: null },
          ].map((item, index) => (
            <Button
              key={index}
              className={classnames(
                'm-4 w-60 flex justify-center',
                item.active
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed',
              )}
              onClick={item.onClick}
            >
              {item.title}
            </Button>
          ))}
        </div>
      </div>
      <div className="w-full lg:w-3/5 md:w-1/2 object-center pt-5 md:pt-0 pl-0 md:pl-5 lg:pl-0">
        <div className="w-full lg:w-3/5 mx-auto h-full flex flex-col justify-center">
          <Card
            title="Your Card"
            description="The finished product!"
            imageSrc={themeSuffix}
            selected
          />
        </div>
      </div>
    </div>
  );
};

DisplayStage.propTypes = {
  userId: PropTypes.string.isRequired,
  themeSuffix: PropTypes.string.isRequired,
};

export default DisplayStage;
