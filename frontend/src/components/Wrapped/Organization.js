import React from 'react';
import PropTypes from 'prop-types';
import { classnames } from '../../utils';

const WrappedSection = (props) => {
  return (
    <div className="w-full h-auto flex flex-wrap mb-8">
      {props.useTitle && <p className="w-screen p-2 text-3xl">{props.title}</p>}
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
      className={classnames(
        'p-2',
        props.height === 96 && 'h-96',
        props.height === 72 && 'h-72',
        props.height === 0 && 'h-auto',
        props.width === '1' && 'w-full',
        props.width === '2/3' && 'w-2/3',
        props.width === '1/2' && 'w-1/2',
        props.width === '1/3' && 'w-1/3',
        props.width === '1/4' && 'w-1/4',
        props.width === '1/5' && 'w-1/5',
        props.width === '1/6' && 'w-1/6',
      )}
    >
      <div
        className={classnames(
          'shadow bg-gray-50 w-full h-full p-8 flex flex-col justify-center',
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
  height: PropTypes.number,
  width: PropTypes.string,
  className: PropTypes.string,
};

WrappedCard.defaultProps = {
  height: 0,
  width: '1',
  className: '',
};

export { WrappedSection, WrappedCard };
