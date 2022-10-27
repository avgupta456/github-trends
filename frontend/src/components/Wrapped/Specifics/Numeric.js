import React from 'react';
import PropTypes from 'prop-types';

import { WrappedCard } from '../Organization';

const numericPropTypes = {
  num: PropTypes.any,
  label: PropTypes.string.isRequired,
};

const numericDefaultProps = {
  num: 'N/A',
};

const NumericPlusLOC = ({ num, label }) => {
  return (
    <WrappedCard>
      <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold w-full text-center text-green-600">{`+${num}`}</p>
      <p className="2xl:text-lg w-full text-center text-green-600">{label}</p>
    </WrappedCard>
  );
};

NumericPlusLOC.propTypes = numericPropTypes;
NumericPlusLOC.defaultProps = numericDefaultProps;

const NumericMinusLOC = ({ num, label }) => {
  return (
    <WrappedCard>
      <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold w-full text-center text-red-600">{`-${num}`}</p>
      <p className="2xl:text-lg w-full text-center text-red-600">{label}</p>
    </WrappedCard>
  );
};

NumericMinusLOC.propTypes = numericPropTypes;
NumericMinusLOC.defaultProps = numericDefaultProps;

const NumericBothLOC = ({ num1, num2, label }) => {
  return (
    <WrappedCard>
      <div className="flex justify-center">
        <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold text-center text-green-600">
          {num1}
        </p>
        <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold mx-2">/</p>
        <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold text-center text-red-600">
          {num2}
        </p>
      </div>
      <p className="2xl:text-lg w-full text-center">{label}</p>
    </WrappedCard>
  );
};

NumericBothLOC.propTypes = {
  num1: PropTypes.any,
  num2: PropTypes.any,
  label: PropTypes.string.isRequired,
};

NumericBothLOC.defaultProps = {
  num1: 'N/A',
  num2: 'N/A',
};

const NumericBestDay = ({
  num,
  date,
  label,
  className,
  onMouseOver,
  onMouseOut,
}) => {
  return (
    <WrappedCard
      className={className}
      onMouseOver={onMouseOver}
      onMouseOut={onMouseOut}
    >
      <div className="h-24 mb-2 flex flex-col justify-center">
        <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold text-center text-green-600">
          {num} Contributions
        </p>
        <p className="text-2xl 2xl:text-3xl 3xl:text-4xl font-bold text-center">
          on {date}
        </p>
      </div>
      <p className="text-lg 2xl:text-xl w-full text-center">{label}</p>
    </WrappedCard>
  );
};

NumericBestDay.propTypes = {
  num: PropTypes.number.isRequired,
  date: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  className: PropTypes.string,
  onMouseOver: PropTypes.func,
  onMouseOut: PropTypes.func,
};

NumericBestDay.defaultProps = {
  className: '',
  onMouseOver: () => {},
  onMouseOut: () => {},
};

export { NumericPlusLOC, NumericMinusLOC, NumericBothLOC, NumericBestDay };
