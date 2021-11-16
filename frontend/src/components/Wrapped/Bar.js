/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveBar } from '@nivo/bar';

import { theme } from './theme';

const BarGraph = ({ data, type, usePrivate }) => {
  const formattedType =
    type === 'contribs' ? 'contribs' : 'formatted_loc_changed';

  const prefix = `${usePrivate ? '' : 'public_'}months`;
  let newData = data[prefix];
  if (!Array.isArray(newData)) {
    newData = [];
  }

  const months = [
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

  return (
    <div className="w-full h-96 p-2">
      <div className="shadow bg-gray-50 w-full h-full p-4 flex flex-col">
        <p className="text-xl font-semibold">Contributions by Month</p>
        <ResponsiveBar
          theme={theme}
          data={newData}
          indexBy="month"
          keys={[type]}
          margin={{ top: 30, right: 0, bottom: 50, left: 80 }}
          padding={0.3}
          layout="vertical"
          colors={{ scheme: 'category10' }}
          // eslint-disable-next-line no-unused-vars
          tooltip={(bar, color, label) => (
            <div
              style={{
                fontSize: '14px',
                padding: 6,
                background: '#fff',
                boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
              }}
            >
              <strong>{months[bar.data.month || 0]}</strong>
              {`: ${bar.data[formattedType]} ${
                type === 'contribs' ? 'Contributions' : ''
              }`}
            </div>
          )}
          axisTop={null}
          axisRight={null}
          axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'Month',
            legendPosition: 'middle',
            legendOffset: 32,
            format: (value) => months[value],
          }}
          axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: type === 'contribs' ? 'Contributions' : 'LOC Changed',
            legendPosition: 'middle',
            legendOffset: -60,
          }}
          label={(d) => d.data[formattedType].split(' ')[0]}
          labelSkipWidth={12}
          labelSkipHeight={12}
          labelTextColor="#fff"
        />
      </div>
    </div>
  );
};

BarGraph.propTypes = {
  data: PropTypes.object,
  type: PropTypes.string.isRequired,
  usePrivate: PropTypes.bool,
};

BarGraph.defaultProps = {
  data: {
    months: [],
    public_months: [],
  },
  usePrivate: false,
};

export default BarGraph;
