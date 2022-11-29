/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { saveSvgAsPng } from 'save-svg-as-png';

import { Card, Button } from '../../../components';
import { classnames } from '../../../utils';

const DisplayStage = ({ userId, themeSuffix }) => {
  const card = themeSuffix.split('?')[0];

  const downloadPNG = () => {
    saveSvgAsPng(document.getElementById('svg-card'), `${userId}_${card}.png`, {
      scale: 2,
      encoderOptions: 1,
    });
  };

  const copyUrl = () => {
    navigator.clipboard.writeText(
      `https://api.githubtrends.io/user/svg/${userId}/${themeSuffix}`,
    );
    toast.info('Copied to Clipboard!', {
      position: 'bottom-right',
      autoClose: 1000,
      hideProgressBar: true,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: false,
      progress: undefined,
    });
  };

  return (
    <div className="w-full flex flex-wrap">
      <ToastContainer />
      <div className="h-auto lg:w-2/5 md:w-1/2 pr-10 p-10 rounded-sm bg-gray-200">
        <div>
          Copy the image URL or download the PNG. Share on GitHub, Twitter,
          LinkedIn, or anywhere else!
        </div>
        <br />
        <div className="flex flex-col items-center">
          {[
            { title: 'Copy URL', active: true, onClick: copyUrl },
            { title: 'Download PNG', active: true, onClick: downloadPNG },
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
            imageSrc={`${themeSuffix}&use_animation=False`}
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
