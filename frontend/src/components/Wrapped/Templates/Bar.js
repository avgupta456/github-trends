/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveBarCanvas } from '@nivo/bar';

import { theme } from './theme';
import { WrappedCard } from '../Organization';

const BarGraph = ({
  data,
  labels,
  xTitle,
  subheader,
  type,
  getLabel,
  legendText,
}) => {
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

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <p className="text-xl font-semibold">Contributions by {xTitle}</p>
        <p>{subheader}</p>
        {Array.isArray(data) && data.length > 0 ? (
          <ResponsiveBarCanvas
            theme={theme}
            colors={getColor}
            data={data}
            indexBy="index"
            keys={[type]}
            margin={{ top: 30, right: 0, bottom: 50, left: 80 }}
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
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            No data to show
          </div>
        )}
      </WrappedCard>
    </div>
  );
};

BarGraph.propTypes = {
  data: PropTypes.array.isRequired,
  labels: PropTypes.array.isRequired,
  xTitle: PropTypes.string.isRequired,
  subheader: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  getLabel: PropTypes.func.isRequired,
  legendText: PropTypes.string.isRequired,
};

export default BarGraph;
