/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveSwarmPlot } from '@nivo/swarmplot';

import { theme } from './theme';

const SwarmPlot = ({ data, usePrivate }) => {
  const prefix = `${usePrivate ? '' : 'public_'}contribs`;
  // eslint-disable-next-line react/prop-types
  const currData = data[prefix];

  console.log(currData);

  return (
    <div className="w-full h-96">
      <ResponsiveSwarmPlot
        theme={theme}
        data={currData}
        groups={['commit', 'issue', 'pr', 'review']}
        groupBy="type"
        identity="id"
        value="timestamp"
        valueFormat="$.2f"
        // valueScale={{ type: 'linear', min: 0, max: 500, reverse: false }}
        // size={{ key: 'volume', values: [4, 20], sizes: [6, 20] }}
        forceStrength={4}
        simulationIterations={100}
        borderColor={{
          from: 'color',
          modifiers: [
            ['darker', 0.6],
            ['opacity', 0.5],
          ],
        }}
        margin={{ top: 80, right: 100, bottom: 80, left: 100 }}
        axisTop={{
          orient: 'top',
          tickSize: 10,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'group if vertical, price if horizontal',
          legendPosition: 'middle',
          legendOffset: -46,
        }}
        axisRight={{
          orient: 'right',
          tickSize: 10,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'price if vertical, group if horizontal',
          legendPosition: 'middle',
          legendOffset: 76,
        }}
        axisBottom={{
          orient: 'bottom',
          tickSize: 10,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'group if vertical, price if horizontal',
          legendPosition: 'middle',
          legendOffset: 46,
        }}
        axisLeft={{
          orient: 'left',
          tickSize: 10,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'price if vertical, group if horizontal',
          legendPosition: 'middle',
          legendOffset: -76,
        }}
      />
    </div>
  );
};

SwarmPlot.propTypes = {
  data: PropTypes.objectOf(
    PropTypes.shape({
      contribs: PropTypes.array,
      public_contribs: PropTypes.array,
    }),
  ),
  usePrivate: PropTypes.bool,
};

SwarmPlot.defaultProps = {
  data: {
    contribs: [],
    public_contribs: [],
  },
  usePrivate: false,
};

export default SwarmPlot;
