import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';

import CopyIcon from 'mdi-react/ContentCopyIcon';

import { classnames } from '../utils';

import './card.css';

const Card = ({ title, description, imageSrc }) => {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (copied) setCopied(false);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [copied]);

  return (
    <div className="p-2 md:w-1/3 sm:mb-0 mb-6">
      <div className="p-4 rounded-lg bg-gray-50 hover:bg-gray-100">
        <div className={classnames('card_container', 'relative')}>
          <img
            alt="content"
            className={classnames('image', 'object-cover h-full w-full')}
            src={imageSrc}
          />
          <button
            type="button"
            className={classnames(
              'overlay',
              'h-full w-full text-blue-500 flex justify-center items-center',
            )}
            onClick={() => {
              navigator.clipboard.writeText(
                `[![GitHub Trends SVG](${imageSrc})](https://githubtrends.io)`,
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
        <h2 className="text-xl font-medium title-font text-gray-900 mt-5">
          {title}
        </h2>
        <p className="text-base leading-relaxed mt-2">{description}</p>
        <Link
          className="text-blue-500 inline-flex items-center p-2 pl-0"
          to="/customize"
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

export default Card;
