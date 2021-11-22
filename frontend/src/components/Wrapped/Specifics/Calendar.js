import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { Input } from '../../Generic';
import { theme } from '../Templates/theme';
import { WrappedCard } from '../Templates/Organization';

const Calendar = ({ data, startDate, endDate }) => {
  const valueOptions = [
    { value: 'contribs', label: 'Contributions', disabled: false },
    { value: 'commits', label: 'Commits', disabled: false },
    { value: 'issues', label: 'Issues', disabled: false },
    { value: 'prs', label: 'Pull Requests', disabled: false },
    { value: 'reviews', label: 'Reviews', disabled: false },
  ];

  // eslint-disable-next-line no-unused-vars
  const [value, setValue] = React.useState(valueOptions[0]);

  // eslint-disable-next-line no-unused-vars
  const [selectedDay, setSelectedDay] = React.useState(null);

  const numEvents = Array.isArray(data)
    ? data.reduce((acc, x) => acc + x[value.value], 0)
    : 0;

  return (
    <WrappedCard height={72}>
      <div className="h-6 flex justify-between items-center">
        <p className="text-xl font-semibold">
          Interactive Contribution Calendar
        </p>
        <Input
          className="w-48 border-2 border-gray-300"
          options={valueOptions}
          selectedOption={value}
          setSelectedOption={setValue}
        />
      </div>
      <div className="h-60 flex flex-col">
        <p className="text-lg">{`${numEvents} ${value.label}`}</p>
        {Array.isArray(data) && data.length > 0 && (
          <ResponsiveCalendar
            theme={theme}
            data={data
              .map((item) => ({
                day: item.day,
                value: item[value.value],
              }))
              .filter((item) => item.value !== 0)}
            from={startDate}
            to={endDate}
            emptyColor="#EBEDF0"
            colors={['#9BE9A8', '#40C463', '#30A14E', '#216E39']}
            margin={{ top: 30, right: 0, bottom: 0, left: 20 }}
            monthBorderColor="#ffffff"
            dayBorderWidth={2}
            dayBorderColor="#ffffff"
            // eslint-disable-next-line no-unused-vars
            onClick={(dayData, event) => {
              setSelectedDay(dayData.day);
            }}
          />
        )}
      </div>
    </WrappedCard>
  );
};

Calendar.propTypes = {
  data: PropTypes.array,
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
};

Calendar.defaultProps = {
  data: [],
};

export default Calendar;
