/* eslint-disable react/no-array-index-key */

import React from 'react';
import PropTypes from 'prop-types';

import { Card } from '../../../components';

const SelectCardStage = ({ selectedCard, setSelectedCard, setStage }) => {
  return (
    <div className="flex flex-wrap">
      {[
        {
          title: 'Language Contributions',
          description: 'See your overall language breakdown',
          imageSrc: 'langs',
        },
        {
          title: 'Repository Contributions',
          description: 'See your most contributed repository by lines of code',
          imageSrc: 'repos',
        },
      ].map((card, index) => (
        <button
          className="w-1/3 p-4"
          key={index}
          type="button"
          onClick={() => {
            if (selectedCard !== card.imageSrc) {
              setSelectedCard(card.imageSrc);
              setStage(1);
            } else {
              setSelectedCard(null);
            }
          }}
        >
          <Card
            title={card.title}
            description={card.description}
            imageSrc={card.imageSrc}
            selected={selectedCard === card.imageSrc}
          />
        </button>
      ))}
    </div>
  );
};

SelectCardStage.propTypes = {
  selectedCard: PropTypes.string.isRequired,
  setSelectedCard: PropTypes.func.isRequired,
  setStage: PropTypes.func.isRequired,
};

export default SelectCardStage;
