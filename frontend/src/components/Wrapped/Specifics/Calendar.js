import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { Input } from '../../Generic';
import { theme } from '../Templates/theme';
import { WrappedCard } from '../Organization';

const Calendar = ({ data, startDate, endDate }) => {
  const newData = data?.calendar_data || [];

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

  const numEvents = Array.isArray(newData)
    ? newData.reduce((acc, x) => acc + x[value.value], 0)
    : 0;

  return (
    <div className="w-full">
      <WrappedCard>
        <div className="h-6 flex justify-between items-center">
          <p className="text-lg lg:text-xl font-semibold">
            Contribution Calendar
          </p>
          <Input
            className="hidden lg:block w-48 border-2 border-gray-300"
            options={valueOptions}
            selectedOption={value}
            setSelectedOption={setValue}
          />
        </div>
        <div className="h-32 lg:h-60 flex flex-col">
          <p className="lg:text-lg">{`${numEvents} ${value.label}`}</p>
          {Array.isArray(newData) && newData.length > 0 ? (
            <ResponsiveCalendar
              theme={theme}
              data={newData
                .map((item) => ({
                  day: item.day,
                  value: item[value.value],
                }))
                .filter((item) => item.value !== 0)}
              from={startDate}
              to={endDate}
              emptyColor="#EBEDF0"
              colors={['#9BE9A8', '#40C463', '#30A14E', '#216E39']}
              margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
              monthBorderColor="#ffffff"
              dayBorderWidth={2}
              dayBorderColor="#ffffff"
              // eslint-disable-next-line no-unused-vars
              onClick={(dayData, event) => {
                setSelectedDay(dayData.day);
              }}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              No data to show
            </div>
          )}
        </div>
      </WrappedCard>
    </div>
  );
};

Calendar.propTypes = {
  data: PropTypes.object.isRequired,
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
};

export default Calendar;
