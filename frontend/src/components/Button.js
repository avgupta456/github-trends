import React from 'react';
import PropTypes from 'prop-types';

import { classnames } from '../utils';

export const Button = (props) => (
  <button
    type="button"
    className={classnames(
      props.className,
      'border-0 py-2 px-6 inline-flex focus:outline-none rounded text-lg',
    )}
  >
    {props.children}
  </button>
);

Button.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node.isRequired,
};

Button.defaultProps = {
  className: '',
};
