import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

import { Input } from '../../Generic';
import { theme, scale } from '../Templates/theme';
import { WrappedCard } from '../Organization';

const Calendar = ({
  data,
  startDate,
  endDate,
  highlightDays,
  highlightColors,
  downloadLoading,
}) => {
  const newData = data?.calendar_data?.days || [];

  const valueOptions = [
    { value: 'contribs', label: 'Contributions', disabled: false },
    { value: 'commits', label: 'Commits', disabled: false },
    { value: 'issues', label: 'Issues', disabled: false },
    { value: 'prs', label: 'Pull Requests', disabled: false },
    { value: 'reviews', label: 'Reviews', disabled: false },
  ];

  const [value, setValue] = React.useState(valueOptions[0]);

  const numEvents = Array.isArray(newData)
    ? newData.reduce((acc, x) => acc + x[value.value], 0)
    : 0;

  let c = 0;
  const max = Math.max(...newData.map((x) => x[value.value]));
  const quantiles = [
    Math.floor(max * 0.25),
    Math.floor(max * 0.5),
    Math.floor(max * 0.75),
    max,
  ];

  const colorScaleFn = (x) => {
    const count = (c % 365) + 1;
    c += 1;

    const myColorScale = highlightDays.includes(count)
      ? highlightColors
      : scale;

    if (x === 0) {
      return myColorScale[0];
    }
    if (x <= quantiles[0]) {
      return myColorScale[1];
    }
    if (x <= quantiles[1]) {
      return myColorScale[2];
    }
    if (x <= quantiles[2]) {
      return myColorScale[3];
    }
    return myColorScale[4];
  };

  return (
    <div className="w-full">
      <WrappedCard>
        <div className="h-6 flex justify-between items-center">
          <p className="text-lg lg:text-xl font-semibold">
            Contribution Calendar
          </p>
          {!downloadLoading && (
            <Input
              className="hidden lg:block w-48 border-2 border-gray-300"
              options={valueOptions}
              selectedOption={value}
              setSelectedOption={setValue}
            />
          )}
        </div>
        <div className="flex flex-col h-48">
          <p className="lg:text-lg">{`${numEvents} ${value.label}`}</p>
          {Array.isArray(newData) && newData.length > 0 ? (
            <ResponsiveCalendar
              theme={theme}
              data={newData.map((item) => ({
                day: item.day,
                value: item[value.value],
              }))}
              from={startDate}
              to={endDate}
              emptyColor="#EBEDF0"
              colors={['#9BE9A8', '#40C463', '#30A14E', '#216E39']}
              margin={{ top: 10, right: 0, bottom: 0, left: 0 }}
              monthBorderColor="#ffffff"
              dayBorderWidth={2}
              dayBorderColor="#ffffff"
              colorScale={colorScaleFn}
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
  highlightDays: PropTypes.arrayOf(PropTypes.number),
  highlightColors: PropTypes.arrayOf(PropTypes.string).isRequired,
  downloadLoading: PropTypes.bool.isRequired,
};

Calendar.defaultProps = {
  highlightDays: [],
};

export default Calendar;
