/* eslint-disable jsx-a11y/interactive-supports-focus */
/* eslint-disable jsx-a11y/click-events-have-key-events */

import React from 'react';
import PropTypes from 'prop-types';

const Checkbox = ({ question, variable, setVariable, disabled }) => {
  return (
    <div
      className="flex inline-row mt-4"
      onClick={() => setVariable(!variable)}
      role="button"
    >
      <input
        type="checkbox"
        disabled={disabled}
        checked={variable && !disabled ? 'checked' : ''}
        className="checkbox mr-2"
        onChange={() => setVariable(!variable)}
      />
      {question}
    </div>
  );
};

Checkbox.propTypes = {
  question: PropTypes.string.isRequired,
  variable: PropTypes.bool.isRequired,
  setVariable: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

Checkbox.defaultProps = {
  disabled: false,
};

export default Checkbox;
