/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { WrappedCard } from '../Organization';

const Numeric = ({ num, label, width }) => {
  return (
    <WrappedCard width={width}>
      <p className="text-2xl font-bold w-full text-center">{num || 'N/A'}</p>
      <p className="w-full text-center">{label}</p>
    </WrappedCard>
  );
};

Numeric.propTypes = {
  num: PropTypes.number.isRequired,
  label: PropTypes.string.isRequired,
  width: PropTypes.string,
};

Numeric.defaultProps = {
  width: '1/3',
};

export default Numeric;
