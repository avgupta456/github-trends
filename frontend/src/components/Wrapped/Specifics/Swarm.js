import React from 'react';
import PropTypes from 'prop-types';

import { SwarmPlot } from '../Templates';

const formatYAxis = (value) => {
  if (value === 3600 * 12) {
    return 'Noon';
  }
  if (value === 3600 * 24) {
    return 'Midnight';
  }
  let hours = Math.floor(value / 3600);
  const suffix = hours % 24 >= 12 ? 'PM' : 'AM';
  hours = hours % 12 === 0 ? 12 : hours % 12;
  const minutes = String(Math.floor((value % 3600) / 60 / 10) * 10);
  const displayHour = String(hours).padStart(2, '0');
  const displayMinute = String(minutes).padStart(2, '0');
  return `${displayHour}:${displayMinute} ${suffix}`;
};

const SwarmType = ({ data }) => {
  const newData = data?.timestamp_data?.contribs || [];

  return (
    <SwarmPlot
      header="Contributions by Time and Type"
      data={newData}
      groupBy="type"
      groups={['commit', 'issue', 'pr', 'review']}
      legend="Contribution Type"
      formatXAxis={(value) => {
        return {
          commit: 'Commits',
          issue: 'Issues',
          pr: 'Pull Requests',
          review: 'Reviews',
        }[value];
      }}
      formatYAxis={formatYAxis}
    />
  );
};

SwarmType.propTypes = {
  data: PropTypes.object.isRequired,
};

const SwarmDay = ({ data }) => {
  const newData = data?.timestamp_data?.contribs || [];

  return (
    <SwarmPlot
      header="Contributions by Time and Day"
      data={newData}
      groupBy="weekday"
      groups={[0, 1, 2, 3, 4, 5, 6]}
      legend="Day of Week"
      formatXAxis={(value) => {
        return {
          0: 'Sunday',
          1: 'Monday',
          2: 'Tuesday',
          3: 'Wednesday',
          4: 'Thursday',
          5: 'Friday',
          6: 'Saturday',
        }[value];
      }}
      formatYAxis={formatYAxis}
    />
  );
};

SwarmDay.propTypes = {
  data: PropTypes.object.isRequired,
};

export { SwarmType, SwarmDay };
