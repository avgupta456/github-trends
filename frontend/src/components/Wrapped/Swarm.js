/* eslint-disable react/prop-types */
/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveSwarmPlot } from '@nivo/swarmplot';

import { theme } from './theme';

const SwarmPlot = ({ data, type, usePrivate }) => {
  const prefix = `${usePrivate ? '' : 'public_'}contribs`;
  const currData = data[prefix];

  const tickValues = [0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => 10800 * i);

  return (
    <div className="w-full h-96">
      <ResponsiveSwarmPlot
        theme={theme}
        isInteractive={false}
        data={currData}
        groupBy={type}
        groups={
          type === 'type'
            ? ['commit', 'issue', 'pr', 'review']
            : [0, 1, 2, 3, 4, 5, 6]
        }
        identity="id"
        value="timestamp"
        size={6}
        forceStrength={4}
        simulationIterations={60}
        colors={{ scheme: 'category10' }}
        gridYValues={tickValues}
        margin={{ top: 20, right: 20, bottom: 80, left: 100 }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          orient: 'bottom',
          tickSize: 10,
          tickPadding: 5,
          tickRotation: 0,
          legend: type === 'type' ? 'Contribution Type' : 'Day of Week',
          legendPosition: 'middle',
          legendOffset: 46,
          format: (value) => {
            return {
              0: 'Sunday',
              1: 'Monday',
              2: 'Tuesday',
              3: 'Wednesday',
              4: 'Thursday',
              5: 'Friday',
              6: 'Saturday',
              commit: 'Commits',
              issue: 'Issues',
              pr: 'Pull Requests',
              review: 'Reviews',
            }[value];
          },
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
          format: (value) => {
            let hours = Math.floor(value / 3600);
            const suffix = hours % 24 > 12 ? 'PM' : 'AM';
            hours = hours % 12 === 0 ? 12 : hours % 12;
            const minutes = String(Math.floor((value % 3600) / 60 / 10) * 10);
            const displayHour = String(hours).padStart(2, '0');
            const displayMinute = String(minutes).padStart(2, '0');
            return `${displayHour}:${displayMinute} ${suffix}`;
          },
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
  type: PropTypes.string,
  usePrivate: PropTypes.bool,
};

SwarmPlot.defaultProps = {
  data: {
    contribs: [],
    public_contribs: [],
  },
  type: 'type',
  usePrivate: false,
};

export default SwarmPlot;
