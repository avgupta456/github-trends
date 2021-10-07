import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';

const PercentSection = ({ usePercent, setUsePercent }) => {
  return (
    <Section title="Use Percent or Lines of Code (LOC)?">
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

PercentSection.propTypes = {
  usePercent: PropTypes.bool.isRequired,
  setUsePercent: PropTypes.func.isRequired,
};

export default PercentSection;
