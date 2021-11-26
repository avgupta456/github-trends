import React from 'react';
import PropTypes from 'prop-types';

import { classnames } from '../../utils';

// options is of form [{value: '', label: '', disabled: true/false}]
const Input = ({
  options,
  selectedOption,
  setSelectedOption,
  disabled,
  className,
}) => {
  return (
    <select
      className={classnames(
        'text-gray-700 bg-white select select-sm w-40 rounded-sm mt-4',
        className,
      )}
      value={selectedOption.label}
      onChange={(e) =>
        setSelectedOption(
          options.find((item) => item.label === e.target.value),
          // eslint-disable-next-line prettier/prettier
        )}
      disabled={disabled}
    >
      {options.map((option) => (
        <option
          key={option.value}
          disabled={option.disabled}
          className={classnames(
            option.label === selectedOption.label && 'bg-blue-200',
          )}
        >
          {option.label}
        </option>
      ))}
    </select>
  );
};

Input.propTypes = {
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      disabled: PropTypes.bool,
    }),
  ).isRequired,
  selectedOption: PropTypes.shape({
    value: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
  }).isRequired,
  setSelectedOption: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  className: PropTypes.string,
};

Input.defaultProps = {
  disabled: false,
  className: '',
};

export default Input;
