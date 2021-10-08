/* eslint-disable react/jsx-props-no-spreading */
/* eslint-disable react/no-danger */

import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

const SvgInline = (props) => {
  const [svg, setSvg] = useState(null);

  useEffect(() => {
    fetch(props.url)
      .then((res) => res.text())
      .then(setSvg);
  }, [props.url]);

  if (props.compact) {
    return (
      <div
        dangerouslySetInnerHTML={{
          __html: `<svg viewBox="0 0 300 175">${svg}</svg>`,
        }}
        {...props}
      />
    );
  }

  return (
    <div
      dangerouslySetInnerHTML={{
        __html: `<svg viewBox="0 0 300 285">${svg}</svg>`,
      }}
      {...props}
    />
  );
};

SvgInline.propTypes = {
  url: PropTypes.string.isRequired,
  compact: PropTypes.bool,
};

SvgInline.defaultProps = {
  compact: false,
};

export default SvgInline;
