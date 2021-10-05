import React from 'react';
import PropTypes from 'prop-types';

import moment from 'moment';

import Section from './Section';

import { classnames } from '../../utils';

const DateRangeSection = ({ selectedTimeRange, setSelectedTimeRange }) => {
  const timeRangeOptions = [
    {
      id: 1,
      name: 'Past 1 Month',
      disabled: false,
      startDate: moment(new Date()).subtract(1, 'month'),
    },
    {
      id: 2,
      name: 'Past 6 Months',
      disabled: false,
      startDate: moment(new Date()).subtract(6, 'month'),
    },
    {
      id: 3,
      name: 'Past 1 Year',
      disabled: false,
      startDate: moment(new Date()).subtract(1, 'year'),
    },
    {
      id: 4,
      name: 'Past 5 Years',
      disabled: false,
      startDate: moment(new Date()).subtract(5, 'year'),
    },
  ];

  const selectedOption = selectedTimeRange || timeRangeOptions[2];

  return (
    <Section title="Date Range">
      <p>Select the date range for statistics.</p>
      <select
        className="select select-sm w-40 rounded mt-4"
        value={selectedOption.name}
        onChange={(e) =>
          setSelectedTimeRange(
            timeRangeOptions.find((item) => item.name === e.target.value),
            // eslint-disable-next-line prettier/prettier
          )}
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
  selectedTimeRange: PropTypes.string.isRequired,
  setSelectedTimeRange: PropTypes.func.isRequired,
};

export default DateRangeSection;
