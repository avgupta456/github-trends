import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import {
  FaArrowRight as ArrowRightIcon,
  FaArrowLeft as ArrowLeftIcon,
} from 'react-icons/fa';

import { classnames } from '../../utils';

const Preview = ({ pages, details, showArrows }) => {
  const totalPages = pages.length;
  const [page, setPage] = useState(0);

  const prevPage = () => {
    setPage((page - 1 + totalPages) % totalPages);
  };

  const nextPage = () => {
    setPage((page + 1 + totalPages) % totalPages);
  };

  useEffect(() => {
    const interval = setInterval(nextPage, 5000);
    return () => clearInterval(interval);
  }, [page]);

  return (
    <div className="w-7/8 mx-auto p-8 rounded-sm">
      <br />
      <div className="flex items-center">
        {showArrows && (
          <ArrowLeftIcon
            className="mr-4 w-8 h-8 text-gray-300 hover:text-gray-600"
            onClick={prevPage}
          />
        )}
        <img
          src={pages[page]}
          alt="preview"
          className={showArrows ? 'w-3/4 mx-auto' : 'w-full'}
        />
        {showArrows && (
          <ArrowRightIcon
            className="ml-4 w-8 h-8 text-gray-300 hover:text-gray-600"
            onClick={nextPage}
          />
        )}
      </div>
      <br />
      <p
        className={classnames(
          'w-full text-center',
          'text-sm lg:text-lg xl:text-xl 2xl:text-2xl',
        )}
      >
        {details[page]}
      </p>
    </div>
  );
};

Preview.propTypes = {
  pages: PropTypes.arrayOf(PropTypes.any).isRequired,
  details: PropTypes.arrayOf(PropTypes.string).isRequired,
  showArrows: PropTypes.bool,
};

Preview.defaultProps = {
  showArrows: true,
};

export default Preview;
