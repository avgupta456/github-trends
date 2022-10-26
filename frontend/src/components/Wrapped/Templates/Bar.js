/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsiveBar } from '@nivo/bar';

import { theme } from './theme';
import { WrappedCard } from '../Organization';

const BarGraph = ({
  data,
  labels,
  xTitle,
  subheader,
  type,
  getTooltip,
  getLabel,
  legendText,
}) => {
  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <p className="text-xl font-semibold">Contributions by Month</p>
        <p>{subheader}</p>
        {Array.isArray(data) && data.length > 0 ? (
          <ResponsiveBar
            theme={theme}
            data={data}
            indexBy="index"
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
                <strong>{labels[bar.data.index || 0]}</strong>
                {`: ${getTooltip(bar.data)}`}
              </div>
            )}
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
  getTooltip: PropTypes.func.isRequired,
  getLabel: PropTypes.func.isRequired,
  legendText: PropTypes.string.isRequired,
};

export default BarGraph;
