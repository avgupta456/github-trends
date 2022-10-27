/* eslint-disable jsx-a11y/mouse-events-have-key-events */

import React from 'react';
import PropTypes from 'prop-types';
import { classnames } from '../../utils';

const WrappedSection = (props) => {
  return (
    <div className="w-full h-auto flex flex-wrap mb-8">
      {props.useTitle && (
        <p className="w-screen p-2 text-2xl lg:text-3xl">{props.title}</p>
      )}
      {props.children}
    </div>
  );
};

WrappedSection.propTypes = {
  useTitle: PropTypes.bool,
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
};

WrappedSection.defaultProps = {
  useTitle: true,
  title: '',
};

const WrappedCard = (props) => {
  return (
    <div
      className="w-full h-full p-1"
      onMouseOver={props.onMouseOver}
      onMouseOut={props.onMouseOut}
    >
      <div
        className={classnames(
          'shadow rounded-sm bg-gray-100 w-full h-full p-4 flex flex-col justify-center',
          props.className,
        )}
      >
        {props.children}
      </div>
    </div>
  );
};

WrappedCard.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  onMouseOver: PropTypes.func,
  onMouseOut: PropTypes.func,
};

WrappedCard.defaultProps = {
  className: '',
  onMouseOver: () => {},
  onMouseOut: () => {},
};

export { WrappedSection, WrappedCard };
