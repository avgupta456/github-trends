/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveBar } from '@nivo/bar';

import { theme } from './theme';
import { WrappedCard } from '../Organization';

const BarGraph = ({
  months,
  subheader,
  type,
  getTooltip,
  getLabel,
  legendText,
}) => {
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

  return (
    <WrappedCard height={96}>
      <p className="text-xl font-semibold">Contributions by Month</p>
      <p>{subheader}</p>
      {Array.isArray(months) && months.length > 0 ? (
        <ResponsiveBar
          theme={theme}
          data={months}
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
              <strong>{monthNames[bar.data.month || 0]}</strong>
              {`: ${getTooltip(bar.data)}`}
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
            format: (value) => monthNames[value],
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
  );
};

BarGraph.propTypes = {
  months: PropTypes.array.isRequired,
  subheader: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  getTooltip: PropTypes.func.isRequired,
  getLabel: PropTypes.func.isRequired,
  legendText: PropTypes.string.isRequired,
};

export default BarGraph;
