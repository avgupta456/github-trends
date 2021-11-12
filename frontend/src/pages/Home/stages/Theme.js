/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { Card } from '../../../components';

const ThemeStage = ({ theme, setTheme, fullSuffix }) => {
  return (
    <div className="flex flex-wrap">
      {[
        {
          title: 'Light Theme',
          description: 'The classic look',
          imageSrc: 'classic',
        },
        {
          title: 'Dark Theme',
          description: 'Coming soon!',
          imageSrc: 'dark',
        },
        {
          title: 'Bright Lights Theme',
          description: 'Coming soon!',
          imageSrc: 'bright_lights',
        },
        {
          title: 'Rosettes',
          description: 'Coming soon!',
          imageSrc: 'rosettes',
        },
        {
          title: 'Ferns',
          description: 'Coming soon!',
          imageSrc: 'ferns',
        },
        {
          title: 'Synthwaves',
          description: 'Coming soon!',
          imageSrc: 'synthwaves',
        },
      ].map((card, index) => (
        <button
          className="w-1/3 p-4"
          key={index}
          type="button"
          onClick={() => setTheme(card.imageSrc)}
        >
          <Card
            title={card.title}
            description={card.description}
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
