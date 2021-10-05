import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';

const UsePercentSection = ({ usePercent, setUsePercent }) => {
  return (
    <Section title="Use Percent?">
      <p>Use lines of code or percents.</p>
      <div className="flex inline-row mt-4">
        <input
          type="checkbox"
          checked={usePercent ? 'checked' : ''}
          className="checkbox mr-2"
          onChange={() => setUsePercent(!usePercent)}
        />
        Use Percent?
      </div>
    </Section>
  );
};

UsePercentSection.propTypes = {
  usePercent: PropTypes.bool.isRequired,
  setUsePercent: PropTypes.func.isRequired,
};

export default UsePercentSection;
