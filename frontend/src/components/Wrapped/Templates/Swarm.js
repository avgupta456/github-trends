/* eslint-disable react/prop-types */
/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveSwarmPlot } from '@nivo/swarmplot';

import { theme } from './theme';
import { WrappedCard } from '../Organization';

const SwarmPlot = ({
  header,
  data,
  groupBy,
  groups,
  legend,
  formatXAxis,
  formatYAxis,
}) => {
  const tickValues = [0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => 10800 * i);

  return (
    <WrappedCard width="2/3" height={96}>
      <p className="text-xl font-semibold">{header}</p>
      <p>{`${data.length} Sampled Contributions`}</p>
      {Array.isArray(data) && data.length > 0 ? (
        <ResponsiveSwarmPlot
          theme={theme}
          isInteractive={false}
          data={data}
          groupBy={groupBy}
          groups={groups}
          identity="id"
          value="timestamp"
          size={6}
          forceStrength={4}
          simulationIterations={60}
          colors={{ scheme: 'category10' }}
          gridYValues={tickValues}
          margin={{ top: 40, right: 0, bottom: 60, left: 100 }}
          axisTop={null}
          axisRight={null}
          axisBottom={{
            orient: 'bottom',
            tickSize: 10,
            tickPadding: 5,
            tickRotation: 0,
            legend,
            legendPosition: 'middle',
            legendOffset: 46,
            format: (value) => formatXAxis(value),
          }}
          axisLeft={{
            orient: 'left',
            tickSize: 10,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'Time of Day',
            legendPosition: 'middle',
            legendOffset: -86,
            tickValues,
            format: (value) => formatYAxis(value),
          }}
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center">
          No data to show
        </div>
      )}
    </WrappedCard>
  );
};

SwarmPlot.propTypes = {
  header: PropTypes.string.isRequired,
  data: PropTypes.array.isRequired,
  groupBy: PropTypes.string.isRequired,
  groups: PropTypes.array.isRequired,
  legend: PropTypes.string.isRequired,
  formatXAxis: PropTypes.func.isRequired,
  formatYAxis: PropTypes.func.isRequired,
};

export default SwarmPlot;
