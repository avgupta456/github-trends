import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';

import { classnames } from '../../utils';

const DateRangeSection = ({
  selectedTimeRange,
  setSelectedTimeRange,
  disabled,
}) => {
  const timeRangeOptions = [
    { id: 1, name: 'Past 1 Month', disabled: false, timeRange: 'one_month' },
    {
      id: 2,
      name: 'Past 3 Months',
      disabled: false,
      timeRange: 'three_months',
    },
    { id: 2, name: 'Past 6 Months', disabled: false, timeRange: 'six_months' },
    { id: 3, name: 'Past 1 Year', disabled: false, timeRange: 'one_year' },
  ];

  const selectedOption = selectedTimeRange || timeRangeOptions[2];

  return (
    <Section title="Date Range">
      <p>Select the date range for statistics.</p>
      <select
        className="text-gray-700 bg-white select select-sm w-40 rounded mt-4"
        value={selectedOption.name}
        onChange={(e) =>
          setSelectedTimeRange(
            timeRangeOptions.find((item) => item.name === e.target.value),
            // eslint-disable-next-line prettier/prettier
          )}
        disabled={disabled}
      >
        {timeRangeOptions.map((option) => (
          <option
            key={option.name}
            disabled={option.disabled}
            className={classnames(
              option.name === selectedOption.name && 'bg-blue-200',
            )}
          >
            {option.name}
          </option>
        ))}
      </select>
    </Section>
  );
};

DateRangeSection.propTypes = {
  selectedTimeRange: PropTypes.object.isRequired,
  setSelectedTimeRange: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

DateRangeSection.defaultProps = {
  disabled: false,
};

export default DateRangeSection;
