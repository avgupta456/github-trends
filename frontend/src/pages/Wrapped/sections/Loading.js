/* eslint-disable react/jsx-one-expression-per-line */

import React, { useState, useEffect } from 'react';

import { PulseLoader } from 'react-spinners';
import Typist from 'react-typist';
import TypistLoop from 'react-typist-loop';

import './loading.css';

const LoadingScreen = () => {
  const [showLoadingMessage, setShowLoadingMessage] = useState(false);
  const [showLoadingErrorMessage, setShowLoadingErrorMessage] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowLoadingMessage(true);
    }, 8000);
    const timer2 = setTimeout(() => {
      setShowLoadingErrorMessage(true);
    }, 50000);
    return () => {
      clearTimeout(timer);
      clearTimeout(timer2);
    };
  }, []);

  return (
    <div className="h-full py-8 flex flex-col justify-center items-center">
      {showLoadingErrorMessage ? (
        <div className="w-96 bg-gray-50 shadow p-4 text-gray-700 text-center text-lg">
          Something went wrong. Please try again in a couple minutes or raise an
          issue on{' '}
          <a
            href="https://github.com/avgupta456/github-trends/issues/new"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 underline"
          >
            GitHub
          </a>
          . Thank you!
        </div>
      ) : (
        <>
          <div className="mb-8">
            <PulseLoader color="#3B82F6" speedMultiplier={0.5} />
          </div>
          {showLoadingMessage ? (
            <TypistLoop interval={200}>
              {[
                'Loading your Data...',
                'Crunching Numbers...',
                'Analyzing Trends...',
                'Drawing Figures...',
                'Almost there!',
              ].map((text, i) => (
                <Typist
                  key={text}
                  cursor={{ blink: true }}
                  className="font-typist text-center text-2xl"
                >
                  <Typist.Delay ms={500 * i} />
                  {text}
                  <Typist.Delay ms={i === 4 ? 20000 : 3000} />
                  <Typist.Backspace count={text.length} />
                </Typist>
              ))}
            </TypistLoop>
          ) : (
            <div className="h-8" />
          )}
        </>
      )}
    </div>
  );
};

export default LoadingScreen;
