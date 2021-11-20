import React from 'react';
import PropTypes from 'prop-types';

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

export { WrappedSection };
