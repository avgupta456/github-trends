import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';
import { Input } from '../Generic';

const DateRangeSection = ({
  selectedTimeRange,
  setSelectedTimeRange,
  disabled,
}) => {
  const timeRangeOptions = [
    { id: 1, label: 'Past 1 Month', disabled: false, value: 'one_month' },
    {
      id: 2,
      label: 'Past 3 Months',
      disabled: false,
      value: 'three_months',
    },
    { id: 2, label: 'Past 6 Months', disabled: false, value: 'six_months' },
    { id: 3, label: 'Past 1 Year', disabled: false, value: 'one_year' },
    { id: 4, label: 'All Time', disabled: false, value: 'all_time' },
  ];

  const selectedOption = selectedTimeRange || timeRangeOptions[2];

  return (
    <Section title="Date Range">
      <p>Select the date range for statistics.</p>
      <Input
        options={timeRangeOptions}
        selectedOption={selectedOption}
        setSelectedOption={setSelectedTimeRange}
        disabled={disabled}
      />
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
