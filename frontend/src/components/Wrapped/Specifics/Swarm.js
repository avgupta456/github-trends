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

const SwarmDay = ({ data }) => {
  let newData = data?.timestamp_data?.contribs || [];
  newData = newData.map((d, i) => {
    return {
      ...d,
      groupById: 0,
      id: i,
    };
  });

  return (
    <SwarmPlot
      header="Contributions by Time"
      data={newData}
      groupBy="groupById"
      groups={[0]}
      legend=""
      formatXAxis={() => ''}
      formatYAxis={formatYAxis}
    />
  );
};

SwarmDay.propTypes = {
  data: PropTypes.object.isRequired,
};

export { SwarmDay };
