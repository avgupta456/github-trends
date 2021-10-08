import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';

const CheckboxSection = ({ title, text, question, variable, setVariable }) => {
  return (
    <Section title={title}>
      <p>{text}</p>
      <div className="flex inline-row mt-4">
        <input
          type="checkbox"
          checked={variable ? 'checked' : ''}
          className="checkbox mr-2"
          onChange={() => setVariable(!variable)}
        />
        {question}
      </div>
    </Section>
  );
};

CheckboxSection.propTypes = {
  title: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  question: PropTypes.string.isRequired,
  variable: PropTypes.bool.isRequired,
  setVariable: PropTypes.func.isRequired,
};

export default CheckboxSection;
