import React from 'react';
import PropTypes from 'prop-types';

import { BarGraph } from '../Templates';

const BarContribs = ({ data }) => {
  const newData = data?.bar_data?.months || [];

  return (
    <BarGraph
      months={newData}
      subheader="By Contribution Count"
      type="contribs"
      getTooltip={(d) => `${d.contribs} Contributions`}
      getLabel={(d) => d.contribs}
      legendText="Contributions"
    />
  );
};

BarContribs.propTypes = {
  data: PropTypes.object.isRequired,
};

const BarLOCChanged = ({ data }) => {
  const newData = data?.bar_data?.months || [];

  return (
    <BarGraph
      months={newData}
      subheader="By Lines of Code Changed"
      type="loc_changed"
      getTooltip={(d) => `${d.formatted_loc_changed}`}
      getLabel={(d) => d.formatted_loc_changed.split(' ')[0]}
      legendText="LOC Changed"
    />
  );
};

BarLOCChanged.propTypes = {
  data: PropTypes.object.isRequired,
};

export { BarContribs, BarLOCChanged };
