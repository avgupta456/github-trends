import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { Checkbox, Input } from '../Generic';
import { theme } from './theme';

const Calendar = ({ startDate, endDate, data }) => {
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
  // eslint-disable-next-line no-unused-vars
  const [usePrivate, setUsePrivate] = React.useState(false);

  const fullValue = usePrivate ? value.value : `public_${value.value}`;
  const fullDisplayValue = `${usePrivate ? 'All' : 'Public'} ${value.label}`;

  // eslint-disable-next-line no-unused-vars
  const [selectedDay, setSelectedDay] = React.useState(null);

  return (
    <div className="flex flex-col w-3/4 mx-auto px-8">
      <p className="text-xl font-semibold">Interactive Contribution Calendar</p>
      <p className="text-lg">{fullDisplayValue}</p>
      <div className="flex justify-around items-center px-8">
        <Input
          className="w-48 h-10 border-2 border-gray-300"
          options={valueOptions}
          selectedOption={value}
          setSelectedOption={setValue}
        />
        <Checkbox
          question="Use Private Contributions?"
          variable={usePrivate}
          setVariable={setUsePrivate}
        />
      </div>
      <div className="h-48">
        <ResponsiveCalendar
          theme={theme}
          data={
            Array.isArray(data)
              ? data
                  .map((item) => ({
                    day: item.day,
                    value: item[fullValue],
                  }))
                  .filter((item) => item.value !== 0)
              : []
          }
          from={startDate}
          to={endDate}
          emptyColor="#EBEDF0"
          colors={['#9BE9A8', '#40C463', '#30A14E', '#216E39']}
          margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
          yearSpacing={40}
          monthBorderColor="#ffffff"
          dayBorderWidth={2}
          dayBorderColor="#ffffff"
          // eslint-disable-next-line no-unused-vars
          onClick={(dayData, event) => {
            setSelectedDay(dayData.day);
          }}
          legends={[
            {
              anchor: 'bottom-right',
              direction: 'row',
              translateY: 36,
              itemCount: 4,
              itemWidth: 42,
              itemHeight: 36,
              itemsSpacing: 14,
              itemDirection: 'right-to-left',
            },
          ]}
        />
      </div>
    </div>
  );
};

Calendar.propTypes = {
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
  data: PropTypes.array,
};

Calendar.defaultProps = {
  data: [],
};

export default Calendar;
