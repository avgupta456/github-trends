import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveRadar } from '@nivo/radar';

import { WrappedCard } from '../Organization';

// eslint-disable-next-line no-unused-vars
const Radar = ({ data }) => {
  const commits = data?.numeric_data?.contribs?.commits || 0;
  const issues = data?.numeric_data?.contribs?.issues || 0;
  const prs = data?.numeric_data?.contribs?.prs || 0;
  const reviews = data?.numeric_data?.contribs?.reviews || 0;

  const tempData = [
    {
      name: 'Commits',
      count: Math.log(1 + commits),
    },
    {
      name: 'Issues',
      count: Math.log(1 + issues),
    },
    {
      name: 'Pull Requests',
      count: Math.log(1 + prs),
    },
    {
      name: 'Reviews',
      count: Math.log(1 + reviews),
    },
  ];

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <p className="text-xl font-semibold">Contributions by Type</p>
        <p>Log Scale</p>
        <ResponsiveRadar
          data={tempData}
          keys={['count']}
          indexBy="name"
          valueFormat={(d) => Math.round(Math.exp(d) - 1)}
          margin={{ top: 30, right: 50, bottom: 30, left: 60 }}
          dotSize={10}
          colors={{ scheme: 'category10' }}
          blendMode="multiply"
          motionConfig="wobbly"
        />
      </WrappedCard>
    </div>
  );
};

Radar.propTypes = {
  data: PropTypes.object.isRequired,
};

export default Radar;
