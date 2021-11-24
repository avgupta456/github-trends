/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

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

export default Numeric;
