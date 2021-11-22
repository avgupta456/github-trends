/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsivePie } from '@nivo/pie';

import { WrappedCard } from './Organization';
import { theme } from './theme';

const PieChart = ({ data, type }) => {
  const currData = data[type];

  return (
    <WrappedCard width="1/3" height={96}>
      <p className="text-xl font-semibold">
        {type.includes('repo')
          ? 'Most Contributed Repositories'
          : 'Most Used Languages'}
      </p>
      <p>{type.includes('changed') ? 'By LOC Modified' : 'By LOC Added'}</p>
      {Array.isArray(currData) && currData.length > 0 && (
        <ResponsivePie
          theme={theme}
          data={currData}
          margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
          innerRadius={0.4}
          padAngle={0.7}
          cornerRadius={3}
          activeOuterRadiusOffset={8}
          borderWidth={1}
          borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
          // Arc Link Settings
          arcLinkLabel={(e) =>
            type.includes('repos')
              ? e.data.label.split('/')[1].replace('repository', 'private')
              : e.data.label
          }
          arcLinkLabelsSkipAngle={45}
          arcLinkLabelsTextOffset={0}
          arcLinkLabelsTextColor={{ from: 'color' }}
          arcLinkLabelsDiagonalLength={5}
          arcLinkLabelsStraightLength={5}
          arcLinkLabelsThickness={0}
          // Arc Label Settings
          arcLabel={(e) => e.data.formatted_value}
          arcLabelsSkipAngle={45}
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
            type.includes('repos')
              ? { scheme: 'category10' }
              : { datum: 'data.color' }
          }
        />
      )}
    </WrappedCard>
  );
};

PieChart.propTypes = {
  data: PropTypes.object,
  type: PropTypes.string,
};

PieChart.defaultProps = {
  data: {
    repos: [],
    public_repos: [],
    langs: [],
    public_langs: [],
  },
  type: 'repos',
};

export default PieChart;
