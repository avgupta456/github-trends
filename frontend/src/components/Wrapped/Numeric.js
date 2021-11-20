/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { WrappedCard } from './Organization';

const Numeric = ({ data, usePrivate, type, label, width }) => {
  let num = 0;
  const prefix = `${usePrivate ? '' : 'public_'}${type}`;
  if (data !== undefined && data[prefix] !== undefined) {
    num = data[prefix];
  }

  return (
    <WrappedCard width={width}>
      <p className="text-2xl font-bold w-full text-center">{num}</p>
      <p className="w-full text-center">{label}</p>
    </WrappedCard>
  );
};

Numeric.propTypes = {
  data: PropTypes.object,
  usePrivate: PropTypes.bool,
  type: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  width: PropTypes.string,
};

Numeric.defaultProps = {
  data: {},
  usePrivate: false,
  width: '1/3',
};

export default Numeric;
