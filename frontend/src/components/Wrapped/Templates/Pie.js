/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { ResponsivePie } from '@nivo/pie';

import { WrappedCard } from '../Organization';
import { theme } from './theme';

const PieChart = ({
  header,
  subheader,
  data,
  getArcLinkLabel,
  getFormattedValue,
  colors,
}) => {
  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <p className="text-lg lg:text-xl font-semibold">{header}</p>
        <p className="lg:text-lg">{subheader}</p>
        {Array.isArray(data) && data.length > 0 ? (
          <ResponsivePie
            theme={theme}
            data={data}
            margin={{ top: 20, right: 40, bottom: 20, left: 40 }}
            innerRadius={0.4}
            padAngle={0.7}
            cornerRadius={3}
            activeOuterRadiusOffset={8}
            borderWidth={1}
            borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
            // Arc Link Settings
            arcLinkLabel={(e) => getArcLinkLabel(e)}
            arcLinkLabelsSkipAngle={45}
            arcLinkLabelsTextOffset={0}
            arcLinkLabelsTextColor={{ from: 'color' }}
            arcLinkLabelsDiagonalLength={5}
            arcLinkLabelsStraightLength={5}
            arcLinkLabelsThickness={0}
            // Arc Label Settings
            arcLabel={(e) => getFormattedValue(e)}
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
                {`: ${getFormattedValue(datum.data)}`}
              </div>
            )}
            colors={colors}
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

PieChart.propTypes = {
  header: PropTypes.string.isRequired,
  subheader: PropTypes.string.isRequired,
  data: PropTypes.array.isRequired,
  getArcLinkLabel: PropTypes.func.isRequired,
  getFormattedValue: PropTypes.func.isRequired,
  colors: PropTypes.any.isRequired,
};

export default PieChart;
