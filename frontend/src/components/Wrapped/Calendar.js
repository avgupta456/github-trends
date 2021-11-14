import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveCalendar } from '@nivo/calendar';

const Calendar = ({ startDate, endDate, data }) => {
  return (
    <ResponsiveCalendar
      data={
        Array.isArray(data)
          ? data
              .map((item) => ({
                day: item.day,
                value: item.loc_added,
              }))
              .filter((item) => item.value !== 0)
          : []
      }
      from={startDate}
      to={endDate}
      emptyColor="#eeeeee"
      colors={['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560']}
      margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
      yearSpacing={40}
      monthBorderColor="#ffffff"
      dayBorderWidth={2}
      dayBorderColor="#ffffff"
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
  );
};

Calendar.propTypes = {
  startDate: PropTypes.string.isRequired,
  endDate: PropTypes.string.isRequired,
  data: PropTypes.array.isRequired,
};

export default Calendar;
