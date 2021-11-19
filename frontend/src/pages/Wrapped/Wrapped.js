/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

import { useParams } from 'react-router-dom';

import { getWrapped } from '../../api';
import {
  BarGraph,
  Calendar,
  Numeric,
  PieChart,
  SwarmPlot,
} from '../../components';
import { Header, LoadingScreen } from './sections';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || 2021;

  const currUserId = useSelector((state) => state.user.userId);
  const currPrivateAccess = useSelector((state) => state.user.privateAccess);
  const usePrivate = currUserId === userId && currPrivateAccess;

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(async () => {
    if (userId.length > 0 && year > 2010 && year <= 2021) {
      const output = await getWrapped(userId, year);
      console.log(output);
      if (output !== null && output !== undefined && output !== {}) {
        setData(output);
        setIsLoading(false);
      }
    }
  }, []);

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
    return <LoadingScreen />;
  }

  return (
    <div className="container px-16 py-8 mx-auto">
      <div className="h-full w-full flex flex-row flex-wrap justify-center items-center">
        <div className="w-full h-auto mb-8">
          <Header
            userId={userId}
            year={year}
            numContribs={contribData.contribs || 'NA'}
            numLines="NA" // TODO: add lines
            currUserId={currUserId}
            usePrivate={usePrivate}
          />
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
