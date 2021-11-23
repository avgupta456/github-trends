import React from 'react';
import PropTypes from 'prop-types';

import { WrappedCard } from '../Organization';

const numericPropTypes = {
  num: PropTypes.any,
  label: PropTypes.string.isRequired,
  width: PropTypes.string,
};

const numericDefaultProps = {
  num: 'N/A',
  width: 'w-1/3',
};

const NumericPlusLOC = ({ num, label, width }) => {
  return (
    <WrappedCard width={width}>
      <p className="text-2xl font-bold w-full text-center text-green-600">{`+${num}`}</p>
      <p className="w-full text-center text-green-600">{label}</p>
    </WrappedCard>
  );
};

NumericPlusLOC.propTypes = numericPropTypes;
NumericPlusLOC.defaultProps = numericDefaultProps;

const NumericMinusLOC = ({ num, label, width }) => {
  return (
    <WrappedCard width={width}>
      <p className="text-2xl font-bold w-full text-center text-red-600">{`-${num}`}</p>
      <p className="w-full text-center text-red-600">{label}</p>
    </WrappedCard>
  );
};

NumericMinusLOC.propTypes = numericPropTypes;
NumericMinusLOC.defaultProps = numericDefaultProps;

const NumericBothLOC = ({ num1, num2, label, width }) => {
  return (
    <WrappedCard width={width}>
      <div className="flex">
        <p className="text-2xl font-bold w-full text-center text-green-600">{`+${num1}`}</p>
        <p className="text-2xl font-bold mx-2">/</p>
        <p className="text-2xl font-bold w-full text-center text-red-600">{`-${num2}`}</p>
      </div>
      <p className="w-full text-center">{label}</p>
    </WrappedCard>
  );
};

NumericBothLOC.propTypes = {
  num1: PropTypes.any,
  num2: PropTypes.any,
  label: PropTypes.string.isRequired,
  width: PropTypes.string,
};

NumericBothLOC.defaultProps = {
  num1: 'N/A',
  num2: 'N/A',
  width: 'w-1/3',
};

export { NumericPlusLOC, NumericMinusLOC, NumericBothLOC };
