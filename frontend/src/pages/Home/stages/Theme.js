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
