/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsivePie } from '@nivo/pie';

import { theme } from './theme';

const PieChart = ({ data, type, usePrivate }) => {
  const prefix = `${usePrivate ? '' : 'public_'}${type}`;

  return (
    <div className="w-full h-96">
      <ResponsivePie
        theme={theme}
        data={data[prefix]}
        margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
        innerRadius={0.5}
        padAngle={0.7}
        cornerRadius={3}
        activeOuterRadiusOffset={8}
        borderWidth={1}
        borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
        // Arc Link Settings
        arcLinkLabel={(e) =>
          type === 'repos'
            ? e.data.label.split('/')[1].replace('repository', 'private')
            : e.data.label
        }
        arcLinkLabelsSkipAngle={30}
        arcLinkLabelsTextOffset={0}
        arcLinkLabelsTextColor={{ from: 'color' }}
        arcLinkLabelsDiagonalLength={5}
        arcLinkLabelsStraightLength={5}
        arcLinkLabelsThickness={0}
        // Arc Label Settings
        arcLabel={(e) => e.data.formatted_value}
        arcLabelsSkipAngle={30}
        arcLabelsTextColor="#fff"
        // Tooltip
        tooltip={({ datum }) => (
          <div
            style={{
              fontSize: '14px',
              padding: 6,
              color: datum.color,
              background: '#fff',
              boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
            }}
          >
            <strong>{datum.label}</strong>
            {`: ${datum.data.formatted_value}`}
          </div>
        )}
        colors={
          type === 'repos' ? { scheme: 'category10' } : { datum: 'data.color' }
        }
      />
    </div>
  );
};

PieChart.propTypes = {
  data: PropTypes.objectOf(
    PropTypes.shape({
      repos: PropTypes.array,
      public_repos: PropTypes.array,
      langs: PropTypes.array,
      public_langs: PropTypes.array,
    }),
  ),
  type: PropTypes.string,
  usePrivate: PropTypes.bool,
};

PieChart.defaultProps = {
  data: {
    repos: [],
    public_repos: [],
    langs: [],
    public_langs: [],
  },
  type: 'repos',
  usePrivate: false,
};

export default PieChart;
