/* eslint-disable react/jsx-props-no-spreading */
/* eslint-disable react/no-danger */

import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const SvgInline = (props) => {
  const [svg, setSvg] = useState(null);

  // eslint-disable-next-line no-unused-vars
  const [loaded, setLoaded] = useState(false);

  let url = `${props.url.split('?')[0]}?cache=${Date.now()}`;
  if (props.url.split('?').length > 1) {
    url += `&${props.url.split('?')[1]}`;
  }

  useEffect(() => {
    setLoaded(false);
    fetch(url)
      .then((res) => res.text())
      .then(setSvg)
      .then(() => setLoaded(true))
      .catch((e) => console.error(e));
  }, [props.url]);

  if (props.forceLoading || !loaded) {
    if (props.compact) {
      return <Skeleton style={{ paddingBottom: '58%' }} />;
    }
    return <Skeleton style={{ paddingBottom: '95%' }} />;
  }

  if (props.compact) {
    return (
      <div
        className={props.className}
        dangerouslySetInnerHTML={{
          __html: `<svg id="svg-card" viewBox="0 0 300 175">${svg}</svg>`,
        }}
      />
    );
  }

  return (
    <div
      className={props.className}
      dangerouslySetInnerHTML={{
        __html: `<svg id="svg-card" viewBox="0 0 300 285">${svg}</svg>`,
      }}
    />
  );
};

SvgInline.propTypes = {
  className: PropTypes.any,
  url: PropTypes.string.isRequired,
  forceLoading: PropTypes.bool,
  compact: PropTypes.bool,
};

SvgInline.defaultProps = {
  className: '',
  forceLoading: false,
  compact: false,
};

export default SvgInline;
