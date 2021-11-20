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
  WrappedSection,
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
        <WrappedSection useTitle={false}>
          <Header
            userId={userId}
            year={year}
            numContribs={contribData.contribs || 'NA'}
            numLines="NA" // TODO: add lines
            currUserId={currUserId}
            usePrivate={usePrivate}
          />
        </WrappedSection>
        <WrappedSection title="Contribution Calendar">
          <Calendar
            data={data.calendar_data}
            startDate={`${year}-01-02`}
            endDate={`${year}-12-31`}
            usePrivate={usePrivate}
          />
          {[
            { data: contribData, type: 'contribs', label: 'Contributions' },
            { data: miscData, type: 'total_days', label: 'With Contributions' },
            { data: miscData, type: 'longest_streak', label: 'Longest Streak' },
          ].map((item) => (
            <Numeric
              key={item.type}
              data={item.data}
              usePrivate={usePrivate}
              type={item.type}
              label={item.label}
              width="1/3"
            />
          ))}
          <BarGraph
            data={data.bar_data}
            type="contribs"
            usePrivate={usePrivate}
          />
        </WrappedSection>
        <WrappedSection title="Contribution Breakdown">
          <SwarmPlot
            data={data.swarm_data}
            type="type"
            usePrivate={usePrivate}
          />
          <div className="w-1/3 flex flex-wrap">
            {[
              { data: contribData, type: 'commits', label: 'Commits' },
              { data: contribData, type: 'issues', label: 'Issues' },
              { data: contribData, type: 'prs', label: 'Pull Requests' },
              { data: contribData, type: 'reviews', label: 'Reviews' },
            ].map((item) => (
              <Numeric
                key={item.type}
                data={item.data}
                usePrivate={usePrivate}
                type={item.type}
                label={item.label}
                width="1/2"
              />
            ))}
          </div>
        </WrappedSection>
        <WrappedSection title="Lines of Code (LOC) Analysis">
          <PieChart
            data={data.pie_data}
            type="repos_added"
            usePrivate={usePrivate}
          />
          <PieChart
            data={data.pie_data}
            type="langs_added"
            usePrivate={usePrivate}
          />
        </WrappedSection>
        <WrappedSection title="Fun Plots and Stats">
          <SwarmPlot
            data={data.swarm_data}
            type="weekday"
            usePrivate={usePrivate}
          />
          <Numeric
            key="weekend_percent"
            data={miscData}
            usePrivate={usePrivate}
            type="weekend_percent"
            label="Weekend Activity"
            width="1/3"
          />
        </WrappedSection>
      </div>
    </div>
  );
};

export default WrappedScreen;
