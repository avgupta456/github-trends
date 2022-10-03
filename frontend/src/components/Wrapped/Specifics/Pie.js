/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';
import { PieChart } from '../Templates';

const PieLangs = ({ data, metric }) => {
  const newData = data?.lang_data?.[`langs_${metric}`] || [];

  return (
    <PieChart
      header="Most Used Languages"
      subheader={metric === 'changed' ? 'By LOC Modified' : 'By LOC Added'}
      data={newData}
      getArcLinkLabel={(e) => e.data.label}
      getFormattedValue={(e) => e.formatted_value}
      colors={{ datum: 'data.color' }}
    />
  );
};

PieLangs.propTypes = {
  data: PropTypes.object.isRequired,
  metric: PropTypes.string.isRequired,
};

const PieRepos = ({ data, metric }) => {
  const newData = data?.repo_data?.[`repos_${metric}`] || [];

  return (
    <PieChart
      header="Most Contributed Repositories"
      subheader={metric === 'changed' ? 'By LOC Modified' : 'By LOC Added'}
      data={newData}
      getArcLinkLabel={({ data: { label } }) => {
        if (label && label.includes('/')) {
          return label.split('/')[1].replace('repository', 'private');
        }
        return label;
      }}
      getFormattedValue={(e) => e.formatted_value}
      colors={{ scheme: 'category10' }}
    />
  );
};

PieRepos.propTypes = {
  data: PropTypes.object.isRequired,
  metric: PropTypes.string.isRequired,
};

export { PieLangs, PieRepos };
