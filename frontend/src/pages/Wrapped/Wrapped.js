/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';

import { getWrapped } from '../../api';
import {
  FloatingIcon,
  WrappedSection,
  Numeric,
  Calendar,
  BarContribs,
  PieLangs,
  PieRepos,
  SwarmType,
  SwarmDay,
} from '../../components';
import { Header, LoadingScreen } from './sections';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || 2021;

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(async () => {
    if (userId?.length > 0 && year > 2010 && year <= 2021) {
      const output = await getWrapped(userId, year);
      if (output !== null && output !== undefined && output !== {}) {
        setData(output);
        setIsLoading(false);
      }
    }
  }, []);

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
            numContribs={data?.numeric_data?.contribs?.contribs || 'NA'}
            numLines={data?.numeric_data?.loc?.loc_changed || 'NA'}
          />
        </WrappedSection>
        <WrappedSection title="Contribution Calendar">
          <Calendar
            data={data}
            startDate={`${year}-01-02`}
            endDate={`${year}-12-31`}
          />
          {[
            {
              num: data?.numeric_data?.contribs?.contribs,
              label: 'Contributions',
            },
            {
              num: data?.numeric_data?.misc?.total_days,
              label: 'With Contributions',
            },
            {
              num: data?.numeric_data?.misc?.longest_streak,
              label: 'Longest Streak',
            },
          ].map((item) => (
            <Numeric
              key={item.type}
              num={item.num}
              label={item.label}
              width="1/3"
            />
          ))}
          <BarContribs data={data} />
        </WrappedSection>
        <WrappedSection title="Contribution Breakdown">
          <SwarmType data={data} />
          <div className="w-1/3 flex flex-wrap">
            {[
              { num: data?.numeric_data?.contribs?.commits, label: 'Commits' },
              { num: data?.numeric_data?.contribs?.issues, label: 'Issues' },
              {
                num: data?.numeric_data?.contribs?.prs,
                label: 'Pull Requests',
              },
              { num: data?.numeric_data?.contribs?.reviews, label: 'Reviews' },
            ].map((item) => (
              <Numeric
                key={item.label}
                num={item.num}
                label={item.label}
                width="1/2"
              />
            ))}
          </div>
        </WrappedSection>
        <WrappedSection title="Lines of Code (LOC) Analysis">
          <PieLangs data={data} metric="added" />
          <PieRepos data={data} metric="added" />
          <div className="w-1/3 flex flex-wrap">
            {[
              {
                num: data?.numeric_data?.loc?.loc_additions,
                label: 'LOC Additions',
              },
              {
                num: data?.numeric_data?.loc?.loc_deletions,
                label: 'LOC Deletions',
              },
              {
                num: data?.numeric_data?.loc?.loc_changed,
                label: 'LOC Changed',
              },
              { num: data?.numeric_data?.loc?.loc_added, label: 'LOC Added' },
            ].map((item) => (
              <Numeric
                key={item.type}
                data={item.data}
                type={item.type}
                label={item.label}
                width="1/2"
              />
            ))}
          </div>
          {[
            {
              num: data?.numeric_data?.loc?.loc_additions_per_commit,
              label: 'LOC Additions per Commit',
            },
            {
              num: data?.numeric_data?.loc?.loc_deletions_per_commit,
              label: 'LOC Deletions per Commit',
            },
            {
              num: data?.numeric_data?.loc?.loc_changed_per_day,
              label: 'LOC Changed per Day',
            },
          ].map((item) => (
            <Numeric
              key={item.type}
              num={item.num}
              label={item.label}
              width="1/3"
            />
          ))}
        </WrappedSection>
        <WrappedSection title="Fun Plots and Stats">
          <SwarmDay data={data} />
          <Numeric
            key="weekend_percent"
            num={data?.numeric_data?.misc?.weekend_percent}
            label="Weekend Activity"
            width="1/3"
          />
        </WrappedSection>
      </div>
      <FloatingIcon />
    </div>
  );
};

export default WrappedScreen;
