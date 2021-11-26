import React, { useState, useEffect } from 'react';

import {
  FaArrowRight as ArrowRightIcon,
  FaArrowLeft as ArrowLeftIcon,
} from 'react-icons/fa';

import avgupta456Langs from '../../assets/avgupta456_langs.png';
import tiangoloRepos from '../../assets/tiangolo_repos.png';
import reininkRepos from '../../assets/reinink_repos.png';
import dhermesLangs from '../../assets/dhermes_langs.png';
import { classnames } from '../../utils';

const Preview = () => {
  const totalPages = 4;
  const pages = [avgupta456Langs, tiangoloRepos, reininkRepos, dhermesLangs];
  const details = [
    'Abhijit Gupta (avgupta456): GitHub Trends',
    'Sebastián Ramírez (tiangolo): FastAPI',
    'Jonathan Reinink (reinink): TailwindCSS',
    'Danny Hermes (dhermes): Google PubSub',
  ];

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
    <div className="w-7/8 mx-auto p-8 my-8 rounded-sm bg-white shadow">
      <p
        className={classnames(
          'text-gray-700 text-xl font-bold',
          'lg:text-xl xl:text-2xl 2xl:text-3xl',
        )}
      >
        Create cards like these...
      </p>
      <br />
      <div className="flex items-center">
        <ArrowLeftIcon
          className="mr-4 w-8 h-8 text-gray-300 hover:text-gray-600"
          onClick={prevPage}
        />
        <img src={pages[page]} alt="preview" className="w-3/4 mx-auto" />
        <ArrowRightIcon
          className="ml-4 w-8 h-8 text-gray-300 hover:text-gray-600"
          onClick={nextPage}
        />
      </div>
      <br />
      <p
        className={classnames(
          'w-full text-center',
          'lg:text-lg xl:text-xl 2xl:text-2xl',
        )}
      >
        {details[page]}
      </p>
    </div>
  );
};

export default Preview;
