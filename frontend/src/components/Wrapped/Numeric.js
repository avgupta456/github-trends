/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

const Numeric = ({ data, usePrivate, type, label }) => {
  let num = 0;
  const prefix = `${usePrivate ? '' : 'public_'}${type}`;
  if (data !== undefined && data[prefix] !== undefined) {
    num = data[prefix];
  }

  return (
    <div className="w-1/5 h-auto p-2">
      <div className="shadow bg-gray-50 w-full h-full p-4 flex flex-col">
        <p className="text-2xl font-bold">{num}</p>
        <p>{label}</p>
      </div>
    </div>
  );
};

Numeric.propTypes = {
  data: PropTypes.object,
  usePrivate: PropTypes.bool,
  type: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};

Numeric.defaultProps = {
  data: {},
  usePrivate: false,
};

export default Numeric;
