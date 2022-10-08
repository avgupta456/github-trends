/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';

import { getWrapped } from '../../api';
import {
  FloatingIcon,
  WrappedSection,
  Numeric,
  NumericOutOf,
  Calendar,
  BarContribs,
  PieLangs,
  PieRepos,
  SwarmType,
  SwarmDay,
  NumericPlusLOC,
  NumericMinusLOC,
  NumericBothLOC,
} from '../../components';
import { Header, LoadingScreen } from './sections';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || '2022';

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [startRange, setStartRange] = useState(0);
  const [endRange, setEndRange] = useState(0);

  useEffect(() => {
    async function getData() {
      if (userId?.length > 0 && year > 2010 && year <= 2022) {
        const output = await getWrapped(userId, year);
        if (output !== null && output !== undefined && output !== {}) {
          setData(output);
          setIsLoading(false);
        }
      }
    }
    getData();
  }, []);

  if (isLoading) {
    return <LoadingScreen />;
  }

  const startStreak = data?.numeric_data?.misc?.longest_streak_days?.[0] || 0;
  const endStreak = data?.numeric_data?.misc?.longest_streak_days?.[1] || 0;
  const startGap = data?.numeric_data?.misc?.longest_gap_days?.[0] || 0;
  const endGap = data?.numeric_data?.misc?.longest_gap_days?.[1] || 0;

  return (
    <div className="container px-2 lg:px-4 xl:px-16 py-2 lg:py-4 xl:py-8 mx-auto">
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
            endDate={`${parseInt(year) + 1}-01-01`}
            startRange={startRange}
            endRange={endRange}
          />
          <div className="w-full flex">
            <NumericOutOf
              num={data?.numeric_data?.contribs?.contribs || 0}
              outOf={1000}
              label="Contributions"
            />
            <NumericOutOf
              num={data?.numeric_data?.misc?.total_days || 0}
              outOf={365}
              label="Days with Contributions"
            />
            <NumericOutOf
              num={data?.numeric_data?.misc?.longest_streak || 0}
              outOf={100}
              label="Longest Streak"
              onClick={() => {
                setStartRange(startStreak);
                setEndRange(endStreak);
              }}
            />
            <NumericOutOf
              num={data?.numeric_data?.misc?.longest_gap || 0}
              outOf={100}
              label="Longest Gap"
              color="#EF4444"
              onClick={() => {
                setStartRange(startGap);
                setEndRange(endGap);
              }}
            />
          </div>
        </WrappedSection>
        <WrappedSection title="Lines of Code (LOC) Analysis">
          <div className="w-full md:w-1/2 xl:w-1/3">
            <PieLangs data={data} metric="changed" />
          </div>
          <div className="w-full md:w-1/2 xl:w-1/3">
            <PieRepos data={data} metric="changed" />
          </div>
          <div className="w-full xl:w-1/3 flex flex-wrap">
            <div className="w-full md:w-1/2 lg:w-1/4 xl:w-1/2">
              <NumericPlusLOC
                num={data?.numeric_data?.loc?.loc_additions}
                label="LOC Additions"
              />
            </div>
            <div className="w-full md:w-1/2 lg:w-1/4 xl:w-1/2">
              <NumericMinusLOC
                num={data?.numeric_data?.loc?.loc_deletions}
                label="LOC Deletions"
              />
            </div>
            <div className="w-full md:w-1/2 lg:w-1/4 xl:w-1/2">
              <NumericBothLOC
                num1={data?.numeric_data?.loc?.loc_additions_per_commit}
                num2={data?.numeric_data?.loc?.loc_deletions_per_commit}
                label="Typical Commit"
              />
            </div>
            <div className="w-full md:w-1/2 lg:w-1/4 xl:w-1/2">
              <Numeric
                num={data?.numeric_data?.loc?.loc_changed_per_day}
                label="Lines Changed Per Day"
              />
            </div>
          </div>
        </WrappedSection>
        <WrappedSection title="Contribution Breakdown">
          <div className="w-full lg:w-1/3 flex flex-wrap">
            {[
              { num: data?.numeric_data?.contribs?.commits, label: 'Commits' },
              { num: data?.numeric_data?.contribs?.issues, label: 'Issues' },
              {
                num: data?.numeric_data?.contribs?.prs,
                label: 'Pull Requests',
              },
              { num: data?.numeric_data?.contribs?.reviews, label: 'Reviews' },
            ].map((item) => (
              <div className="w-full md:w-1/2" key={item.label}>
                <Numeric num={item.num} label={item.label} />
              </div>
            ))}
          </div>
          <div className="w-full lg:w-2/3">
            <SwarmType data={data} />
          </div>
        </WrappedSection>
        <WrappedSection title="Fun Plots and Stats">
          <div className="w-full lg:w-2/3">
            <SwarmDay data={data} />
          </div>
          <div className="w-full lg:w-1/3">
            <Numeric
              key="weekend_percent"
              num={data?.numeric_data?.misc?.weekend_percent}
              label="Weekend Activity"
            />
          </div>
          <BarContribs data={data} />
        </WrappedSection>
      </div>
      <FloatingIcon />
    </div>
  );
};

export default WrappedScreen;
