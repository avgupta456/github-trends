/* eslint-disable jsx-a11y/mouse-events-have-key-events */

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

const NumericOutOf = ({
  num,
  outOf,
  format,
  label,
  color,
  className,
  onMouseOver,
  onMouseOut,
}) => {
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
        className="text-2xl 2xl:text-3xl font-bold"
      >
        {format(total)}
      </text>
    );
  };
  return (
    <WrappedCard
      className={className}
      onMouseOver={onMouseOver}
      onMouseOut={onMouseOut}
    >
      <div className="w-full h-24 mb-2">
        <ResponsivePie
          data={[
            { id: '1', value: num, color },
            { id: '2', value: outOf - num, color: '#d1d5db' },
          ]}
          innerRadius={0.8}
          enableArcLabels={false}
          enableArcLinkLabels={false}
          colors={{ datum: 'data.color' }}
          layers={['arcs', CenteredMetric]}
          tooltip={() => null}
        />
      </div>
      <p className="text-lg 2xl:text-xl w-full text-center">{label}</p>
    </WrappedCard>
  );
};

NumericOutOf.propTypes = {
  num: PropTypes.number.isRequired,
  outOf: PropTypes.number.isRequired,
  format: PropTypes.func,
  label: PropTypes.string.isRequired,
  color: PropTypes.string,
  className: PropTypes.string,
  onMouseOver: PropTypes.func,
  onMouseOut: PropTypes.func,
};

NumericOutOf.defaultProps = {
  format: (x) => x,
  color: '#30A14E',
  className: '',
  onMouseOver: () => {},
  onMouseOut: () => {},
};

export { Numeric, NumericOutOf };
