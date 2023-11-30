import React from 'react';
import PropTypes from 'prop-types';

import Section from './Section';
import { Input } from '../Generic';

const DateRangeSection = ({
  selectedTimeRange,
  setSelectedTimeRange,
  // eslint-disable-next-line no-unused-vars
  privateAccess,
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
    // { id: 4, label: 'All Time', disabled: !privateAccess, value: 'all_time' },
    { id: 4, label: 'All Time', disabled: true, value: 'all_time' },
  ];

  const selectedOption = selectedTimeRange || timeRangeOptions[2];

  return (
    <Section title="Date Range">
      <p>Select the date range for statistics.</p>
      <Input
        options={timeRangeOptions}
        selectedOption={selectedOption}
        setSelectedOption={setSelectedTimeRange}
      />
    </Section>
  );
};

DateRangeSection.propTypes = {
  selectedTimeRange: PropTypes.object.isRequired,
  setSelectedTimeRange: PropTypes.func.isRequired,
  privateAccess: PropTypes.bool.isRequired,
};

export default DateRangeSection;
