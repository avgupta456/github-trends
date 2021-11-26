/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { Card } from '../../../components';

const ThemeStage = ({ theme, setTheme, fullSuffix }) => {
  return (
    <div className="flex flex-wrap">
      {[
        {
          title: 'Classic',
          imageSrc: 'classic',
        },
        {
          title: 'Dark',
          imageSrc: 'dark',
        },
        {
          title: 'Bright Lights',
          imageSrc: 'bright_lights',
        },
        {
          title: 'Rosettes',
          imageSrc: 'rosettes',
        },
        {
          title: 'Ferns',
          imageSrc: 'ferns',
        },
        {
          title: 'Synthwaves',
          imageSrc: 'synthwaves',
        },
      ].map((card, index) => (
        <button
          className="w-full sm:w-1/2 lg:w-1/3 p-2 lg:p-4"
          key={index}
          type="button"
          onClick={() => setTheme(card.imageSrc)}
        >
          <Card
            title={card.title}
            description=""
            imageSrc={`${fullSuffix}&theme=${card.imageSrc}`}
            selected={theme === card.imageSrc}
          />
        </button>
      ))}
    </div>
  );
};

ThemeStage.propTypes = {
  theme: PropTypes.string.isRequired,
  setTheme: PropTypes.func.isRequired,
  fullSuffix: PropTypes.string.isRequired,
};

export default ThemeStage;
