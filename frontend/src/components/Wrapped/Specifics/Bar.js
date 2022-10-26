import React from 'react';
import PropTypes from 'prop-types';

import { BarGraph } from '../Templates';

const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

const dayNames = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];

const BarMonthContribs = ({ data }) => {
  const newData = data?.month_data?.months || [];

  return (
    <BarGraph
      data={newData}
      labels={monthNames}
      xTitle="Month"
      subheader="By Contribution Count"
      type="contribs"
      getLabel={(d) => d.contribs}
      legendText="Contributions"
    />
  );
};

BarMonthContribs.propTypes = {
  data: PropTypes.object.isRequired,
};

const BarDayContribs = ({ data }) => {
  const newData = data?.day_data?.days || [];

  return (
    <BarGraph
      data={newData}
      labels={dayNames}
      xTitle="Day"
      subheader="By Contribution Count"
      type="contribs"
      getLabel={(d) => d.contribs}
      legendText="Contributions"
    />
  );
};

BarDayContribs.propTypes = {
  data: PropTypes.object.isRequired,
};

const BarLOCChanged = ({ data }) => {
  const newData = data?.month_data?.months || [];

  return (
    <BarGraph
      data={newData}
      labels={monthNames}
      xTitle="Month"
      subheader="By Lines of Code Changed"
      type="loc_changed"
      getLabel={(d) => d.formatted_loc_changed.split(' ')[0]}
      legendText="LOC Changed"
    />
  );
};

BarLOCChanged.propTypes = {
  data: PropTypes.object.isRequired,
};

export { BarMonthContribs, BarDayContribs, BarLOCChanged };
