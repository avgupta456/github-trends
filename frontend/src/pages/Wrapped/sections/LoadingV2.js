/* eslint-disable no-else-return */
import React, { useEffect, useState } from 'react';

import { SquareLoader } from 'react-spinners';

const LoadingScreen = () => {
  const months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'June',
    'July',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ];

  // Should take max ~45 seconds, added extra 10 seconds to Dec wait time
  const waitTime = [
    2000, 2000, 2000, 2000, 3000, 3000, 3000, 4000, 4000, 4000, 6000, 20000,
  ];

  const [currMonth, setCurrMonth] = useState(0);

  // increment currMonth every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrMonth(currMonth + 1);
    }, waitTime[currMonth]);
    return () => clearInterval(interval);
  }, [currMonth]);

  const getTile = (i) => {
    if (i < currMonth) {
      return (
        <div
          key={months[i]}
          className="w-16 h-16 rounded bg-blue-500 m-1.5 text-center flex flex-col justify-center"
        >
          <div className="text-white">{months[i]}</div>
        </div>
      );
    } else if (i === currMonth) {
      return (
        <SquareLoader
          key={months[i]}
          color="#3A82F6"
          speedMultiplier={0.75}
          size={64}
          className="rounded bg-blue-500 m-1.5"
        />
      );
    } else {
      return (
        <div
          key={months[i]}
          className="w-16 h-16 rounded bg-gray-500 m-1.5 text-center flex flex-col justify-center"
        >
          <div className="text-white">{months[i]}</div>
        </div>
      );
    }
  };

  return (
    <div className="h-full py-8 flex flex-col justify-center items-center">
      {currMonth < 12 ? (
        <>
          <div>Querying the GitHub API by Months</div>
          <div className="flex flex-wrap m-4 justify-center">
            <div className="flex flex-wrap justify-center">
              <div className="flex">
                {Array.from({ length: 3 }).map((_, i) => getTile(i))}
              </div>
              <div className="flex">
                {Array.from({ length: 3 }).map((_, i) => getTile(i + 3))}
              </div>
            </div>
            <div className="flex flex-wrap justify-center">
              <div className="flex">
                {Array.from({ length: 3 }).map((_, i) => getTile(i + 6))}
              </div>
              <div className="flex">
                {Array.from({ length: 3 }).map((_, i) => getTile(i + 9))}
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="w-4/5 lg:w-1/3 bg-gray-50 shadow p-4 text-gray-700 text-center text-lg">
          Loading your data is taking longer than expected. Try refreshing the
          page, and if that fails, raise an issue on{' '}
          <a
            href="https://github.com/avgupta456/github-trends/issues/new"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 underline"
          >
            GitHub
          </a>
          . Thank you for your patience!
        </div>
      )}
    </div>
  );
};

export default LoadingScreen;
