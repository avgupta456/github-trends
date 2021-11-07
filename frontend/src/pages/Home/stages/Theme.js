/* eslint-disable react/no-array-index-key */
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import { Card } from '../../../components';

const ThemeStage = ({ fullSuffix, setThemeSuffix }) => {
  const [selectedTheme, setSelectedTheme] = useState('light');

  useEffect(() => {
    setThemeSuffix(`${fullSuffix}&theme=${selectedTheme}`);
  }, [fullSuffix, selectedTheme]);

  return (
    <div className="flex flex-wrap">
      {[
        {
          title: 'Light Theme',
          description: 'The classic look',
          imageSrc: 'light',
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
          onClick={() => setSelectedTheme(card.imageSrc)}
        >
          <Card
            title={card.title}
            description={card.description}
            imageSrc={`${fullSuffix}&theme=${card.imageSrc}`}
            selected={selectedTheme === card.imageSrc}
          />
        </button>
      ))}
    </div>
  );
};

ThemeStage.propTypes = {
  fullSuffix: PropTypes.string.isRequired,
  setThemeSuffix: PropTypes.func.isRequired,
};

export default ThemeStage;
