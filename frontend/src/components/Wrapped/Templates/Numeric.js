import React from 'react';
import PropTypes from 'prop-types';

import { ResponsivePie } from '@nivo/pie';

import { WrappedCard } from '../Organization';

const Numeric = ({ num, label }) => {
  return (
    <WrappedCard>
      <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold w-full text-center">
        {num || 'N/A'}
      </p>
      <p className="2xl:text-lg w-full text-center">{label}</p>
    </WrappedCard>
  );
};

Numeric.propTypes = {
  num: PropTypes.any,
  label: PropTypes.string.isRequired,
};

Numeric.defaultProps = {
  num: 'N/A',
};

const NumericOutOf = ({ num, outOf, label }) => {
  // eslint-disable-next-line react/prop-types
  const CenteredMetric = ({ dataWithArc, centerX, centerY }) => {
    let total = 0;
    // eslint-disable-next-line react/prop-types
    dataWithArc.forEach((datum) => {
      total += datum.id === '1' ? datum.value : 0;
    });

    return (
      <text
        x={centerX}
        y={centerY}
        textAnchor="middle"
        dominantBaseline="central"
        className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold"
      >
        {total}
      </text>
    );
  };
  return (
    <WrappedCard>
      <div className="w-full h-32 mb-4">
        <ResponsivePie
          data={[
            { id: '1', value: num, color: '#30A14E' },
            { id: '2', value: outOf - num, color: '#E5E7EB' },
          ]}
          innerRadius={0.8}
          enableArcLabels={false}
          enableArcLinkLabels={false}
          activeInnerRadiusOffset={8}
          activeOuterRadiusOffset={0}
          colors={{ datum: 'data.color' }}
          layers={['arcs', CenteredMetric]}
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
              <strong>
                {datum.value} / {outOf}
              </strong>
            </div>
          )}
        />
      </div>
      <p className="text-lg 2xl:text-xl w-full text-center">{label}</p>
    </WrappedCard>
  );
};

NumericOutOf.propTypes = {
  num: PropTypes.number.isRequired,
  outOf: PropTypes.number.isRequired,
  label: PropTypes.string.isRequired,
};

export { Numeric, NumericOutOf };
