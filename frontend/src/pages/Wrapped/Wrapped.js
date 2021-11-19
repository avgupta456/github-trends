/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';
import { PulseLoader } from 'react-spinners';
import Typist from 'react-typist';
import TypistLoop from 'react-typist-loop';

import { getWrapped } from '../../api';
import {
  Checkbox,
  BarGraph,
  Calendar,
  Numeric,
  PieChart,
  SwarmPlot,
} from '../../components';
import './loading.css';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || 2021;

  const [refresh, setRefresh] = useState(0);
  const [data, setData] = useState({});

  const [isLoading, setIsLoading] = useState(true);
  const [showLoadingMessage, setShowLoadingMessage] = useState(false);
  const [showLoadingErrorMessage, setShowLoadingErrorMessage] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowLoadingMessage(true);
    }, 8000);
    const timer2 = setTimeout(() => {
      setShowLoadingErrorMessage(true);
    }, 32000);
    return () => {
      clearTimeout(timer);
      clearTimeout(timer2);
    };
  }, []);

  useEffect(async () => {
    if (
      isLoading &&
      !showLoadingErrorMessage &&
      userId.length > 0 &&
      year > 2010 &&
      year <= 2021
    ) {
      const output = await getWrapped(userId, year);
      console.log(output);
      if (output !== null && output !== undefined && output !== {}) {
        setData(output);
        setIsLoading(false);
      } else {
        setTimeout(() => {
          setRefresh(refresh + 1);
        }, 10000);
      }
    }
  }, [refresh]);

  const [usePrivate, setUsePrivate] = useState(false);

  let contribData = {};
  try {
    contribData = data.numeric_data.contribs;
  } catch (e) {
    // do nothing
  }

  let miscData = {};
  try {
    miscData = data.numeric_data.misc;
  } catch (e) {
    // do nothing
  }

  if (isLoading) {
    return (
      <div className="h-full py-8 flex flex-col justify-center items-center">
        {showLoadingErrorMessage ? (
          <div className="w-96 bg-gray-50 shadow p-4 text-gray-700 text-center text-lg">
            Something went wrong. Please try again in a couple minutes or raise
            an issue on{' '}
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
              <TypistLoop interval={2000}>
                {[
                  'Crunching Numbers...',
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
                    <Typist.Delay ms={3000} />
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
  }

  return (
    <div className="container px-32 py-16 mx-auto">
      <div className="h-full w-full flex flex-row flex-wrap justify-center items-center">
        <div className="w-full h-32 p-2">
          <div className="shadow bg-gray-50 w-full h-full p-4 flex flex-col">
            <p className="text-2xl font-semibold">
              {`${userId} GitHub Wrapped`}
            </p>
            <Checkbox
              question="Use Private Contributions?"
              variable={usePrivate}
              setVariable={setUsePrivate}
            />
          </div>
        </div>
        {[
          { type: 'contribs', label: 'Contributions' },
          { type: 'commits', label: 'Commits' },
          { type: 'issues', label: 'Issues' },
          { type: 'prs', label: 'Pull Requests' },
          { type: 'reviews', label: 'Reviews' },
        ].map((item) => (
          <Numeric
            key={item.type}
            data={contribData}
            usePrivate={usePrivate}
            type={item.type}
            label={item.label}
            width="1/5"
          />
        ))}
        <Calendar
          data={data.calendar_data}
          startDate={`${year}-01-02`}
          endDate={`${year}-12-31`}
          usePrivate={usePrivate}
        />

        {[
          { type: 'total_days', label: 'With Contributions' },
          { type: 'longest_streak', label: 'Longest Streak' },
          { type: 'weekend_percent', label: 'Weekend Activity' },
        ].map((item) => (
          <Numeric
            key={item.type}
            data={miscData}
            usePrivate={usePrivate}
            type={item.type}
            label={item.label}
          />
        ))}
        <PieChart
          data={data.pie_data}
          type="repos_added"
          usePrivate={usePrivate}
        />
        <SwarmPlot data={data.swarm_data} type="type" usePrivate={usePrivate} />
        <SwarmPlot
          data={data.swarm_data}
          type="weekday"
          usePrivate={usePrivate}
        />
        <PieChart
          data={data.pie_data}
          type="langs_added"
          usePrivate={usePrivate}
        />
        <BarGraph
          data={data.bar_data}
          type="loc_changed"
          usePrivate={usePrivate}
        />
      </div>
    </div>
  );
};

export default WrappedScreen;
