/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveBar } from '@nivo/bar';

import { theme } from './theme';

const BarGraph = ({ data, labels, xTitle, type, getLabel, legendText }) => {
  const maxData = Math.max(...data.map((d) => d[type]));
  const minData = Math.min(
    ...data.filter((d) => d.index < 11).map((d) => d[type]),
  );

  const getColor = (d) => {
    // eslint-disable-next-line no-nested-ternary
    return d.value === maxData
      ? '#2BA02C'
      : d.value === minData
      ? '#D62728'
      : '#468CBF';
  };

  if (!(Array.isArray(data) && data.length > 0)) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        No data to show
      </div>
    );
  }

  return (
    <ResponsiveBar
      theme={theme}
      colors={getColor}
      data={data}
      indexBy="index"
      keys={[type]}
      margin={{ top: 30, right: 0, bottom: 40, left: 80 }}
      padding={0.3}
      layout="vertical"
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: xTitle,
        legendPosition: 'middle',
        legendOffset: 32,
        format: (value) => labels[value],
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: legendText,
        legendPosition: 'middle',
        legendOffset: -60,
      }}
      label={(d) => getLabel(d.data)}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor="#fff"
      tooltip={() => null}
    />
  );
};

BarGraph.propTypes = {
  data: PropTypes.array.isRequired,
  labels: PropTypes.array.isRequired,
  xTitle: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  getLabel: PropTypes.func.isRequired,
  legendText: PropTypes.string.isRequired,
};

export default BarGraph;
