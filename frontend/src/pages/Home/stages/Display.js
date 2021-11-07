/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { Card, Button } from '../../../components';
import { classnames } from '../../../utils';

const DisplayStage = ({ themeSuffix }) => {
  return (
    <div className="w-full flex flex-wrap">
      <div className="h-auto lg:w-2/5 md:w-1/2 pr-10 p-10 rounded bg-gray-100">
        <div>
          Share your GitHub Trends card through multiple channels, including
          GitHub, Twitter, and Linkedin. Or, download the PNG and share
          anywhere!
        </div>
        <br />
        <div className="flex flex-col items-center">
          {[
            { title: 'Display on GitHub', active: true },
            { title: 'Share on Twitter', active: false },
            { title: 'Share on LinkedIn', active: false },
            { title: 'Download PNG', active: false },
          ].map((item, index) => (
            <Button
              key={index}
              className={classnames(
                'm-4 w-60 flex justify-center',
                item.active
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed',
              )}
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
  themeSuffix: PropTypes.string.isRequired,
};

export default DisplayStage;
