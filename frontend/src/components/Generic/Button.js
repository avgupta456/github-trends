/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import PropTypes from 'prop-types';

import { classnames } from '../../utils';

const Button = (props) => {
  return (
    <button
      type="button"
      {...props}
      className={classnames(
        props.className,
        'border-0 py-2 px-6 inline-flex focus:outline-none rounded-sm text-lg',
      )}
    >
      {props.children}
    </button>
  );
};

Button.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node.isRequired,
};

Button.defaultProps = {
  className: '',
};

export default Button;
