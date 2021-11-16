import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { Input } from '../Generic';
import { theme } from './theme';

const Calendar = ({ data, startDate, endDate, usePrivate }) => {
  const valueOptions = [
    { value: 'contribs', label: 'Contributions', disabled: false },
    { value: 'commits', label: 'Commits', disabled: false },
    { value: 'issues', label: 'Issues', disabled: false },
    { value: 'prs', label: 'Pull Requests', disabled: false },
    { value: 'reviews', label: 'Reviews', disabled: false },
    { value: 'loc_added', label: 'Lines of Code Added', disabled: false },
    { value: 'loc_changed', label: 'Lines of Code Changed', disabled: false },
  ];

  // eslint-disable-next-line no-unused-vars
  const [value, setValue] = React.useState(valueOptions[0]);

  const fullValue = usePrivate ? value.value : `public_${value.value}`;
  const fullDisplayValue = `${usePrivate ? 'All' : 'Public'} ${value.label}`;

  // eslint-disable-next-line no-unused-vars
  const [selectedDay, setSelectedDay] = React.useState(null);

  const numEvents = Array.isArray(data)
    ? data.reduce((acc, x) => acc + x[fullValue], 0)
    : 0;

  return (
    <div className="w-full h-72 p-2">
      <div className="shadow bg-gray-50 w-full h-full p-4 flex flex-col">
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
          <p className="text-lg">{`${numEvents} ${fullDisplayValue}`}</p>
          {Array.isArray(data) && data.length > 0 && (
            <ResponsiveCalendar
              theme={theme}
              data={data
                .map((item) => ({
                  day: item.day,
                  value: item[fullValue],
                }))
                .filter((item) => item.value !== 0)}
              from={startDate}
              to={endDate}
              emptyColor="#EBEDF0"
              colors={['#9BE9A8', '#40C463', '#30A14E', '#216E39']}
              margin={{ top: 0, right: 0, bottom: 0, left: 20 }}
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
      </div>
    </div>
  );
};

Calendar.propTypes = {
  data: PropTypes.array,
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
  usePrivate: PropTypes.bool,
};

Calendar.defaultProps = {
  data: [],
  usePrivate: false,
};

export default Calendar;
