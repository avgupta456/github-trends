import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';

const PrivateSection = ({ usePrivate, setUsePrivate }) => {
  return (
    <Section title="Use Private Commits?">
      <div className="flex inline-row mt-4">
        <input
          type="checkbox"
          checked={usePrivate ? 'checked' : ''}
          className="checkbox mr-2"
          onChange={() => setUsePrivate(!usePrivate)}
        />
        Use private commits?
      </div>
    </Section>
  );
};

PrivateSection.propTypes = {
  usePrivate: PropTypes.bool.isRequired,
  setUsePrivate: PropTypes.func.isRequired,
};

export default PrivateSection;
