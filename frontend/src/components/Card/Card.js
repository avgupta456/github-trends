import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';

import Skeleton from 'react-loading-skeleton';

import CopyIcon from 'mdi-react/ContentCopyIcon';

import { classnames } from '../../utils';
import { BACKEND_URL } from '../../constants';

import './card.css';
import SVG from './SVG';

export const Image = ({ imageSrc }) => {
  const userId = useSelector((state) => state.user.userId);

  const [loaded, setLoaded] = useState(false);
  const [copied, setCopied] = useState(false);

  const fullImageSrc = `${BACKEND_URL}/user/svg/${userId}/${imageSrc}`;

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (copied) setCopied(false);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [copied]);

  const image = (
    <div className={classnames('card_container', 'relative')}>
      <div className="h-full w-full relative">
        <SVG
          className={classnames('object-cover h-full w-full', 'image')}
          url={fullImageSrc}
        />
      </div>
      <button
        type="button"
        className={classnames(
          'overlay',
          'h-full w-full text-blue-500 flex justify-center items-center',
        )}
        onClick={() => {
          navigator.clipboard.writeText(
            `[![GitHub Trends SVG](${fullImageSrc})](https://githubtrends.io)`,
          );
          setCopied(true);
        }}
      >
        {copied ? (
          'Copied Link!'
        ) : (
          <>
            Copy Link
            <CopyIcon className="ml-1" />
          </>
        )}
      </button>
    </div>
  );

  return (
    <div>
      <img
        alt="content"
        className="h-0 w-0"
        src={fullImageSrc}
        onLoad={() => setLoaded(true)}
      />
      {loaded ? image : <Skeleton style={{ paddingBottom: '95%' }} />}
    </div>
  );
};

Image.propTypes = {
  imageSrc: PropTypes.string.isRequired,
};

export const Card = ({ title, description, imageSrc }) => {
  return (
    <div>
      <div className="p-4 rounded-lg bg-gray-50 hover:bg-gray-100">
        <Image imageSrc={imageSrc} />
        <h2 className="text-xl font-medium title-font text-gray-900 mt-5">
          {title}
        </h2>
        <p className="text-base leading-relaxed mt-2">{description}</p>
        <Link
          className="text-blue-500 inline-flex items-center p-2 pl-0"
          to={`/customize/${imageSrc}`}
        >
          Customize
          <svg
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="w-4 h-4 ml-2"
            viewBox="0 0 24 24"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

Card.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  imageSrc: PropTypes.string.isRequired,
};
