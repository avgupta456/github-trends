/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';
import { classnames } from '../../utils';

const Numeric = ({ data, usePrivate, type, label, width }) => {
  let num = 0;
  const prefix = `${usePrivate ? '' : 'public_'}${type}`;
  if (data !== undefined && data[prefix] !== undefined) {
    num = data[prefix];
  }

  return (
    <div
      className={classnames(
        'h-auto p-2',
        width === '1' && 'w-full',
        width === '1/2' && 'w-1/2',
        width === '1/3' && 'w-1/3',
        width === '1/4' && 'w-1/4',
        width === '1/5' && 'w-1/5',
        width === '1/6' && 'w-1/6',
      )}
    >
      <div className="shadow bg-gray-50 w-full h-full p-4 flex flex-col justify-center">
        <p className="text-2xl font-bold w-full text-center">{num}</p>
        <p className="w-full text-center">{label}</p>
      </div>
    </div>
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
