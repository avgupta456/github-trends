/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft as LeftArrowIcon } from 'react-icons/fa';

import { getWrapped } from '../../api';
import {
  FloatingIcon,
  WrappedSection,
  Numeric,
  NumericOutOf,
  Calendar,
  hoverScale,
  singleHoverScale,
  BarMonth,
  BarDay,
  PieLangs,
  PieRepos,
  SwarmDay,
  NumericPlusLOC,
  NumericMinusLOC,
  NumericBothLOC,
  NumericBestDay,
} from '../../components';
import Radar from '../../components/Wrapped/Specifics/Radar';
import { LoadingScreen } from './sections';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || '2022';

  const currUserId = useSelector((state) => state.user.userId);
  const usePrivate = useSelector((state) => state.user.privateAccess);

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [highlightDays, setHighlightDays] = useState([]);
  const [highlightColors, setHighlightColors] = useState(hoverScale);

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
  }, [userId, year]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  const startStreak = data?.numeric_data?.misc?.longest_streak_days?.[0] || 0;
  const endStreak = data?.numeric_data?.misc?.longest_streak_days?.[1] || 0;
  const startGap = data?.numeric_data?.misc?.longest_gap_days?.[0] || 0;
  const endGap = data?.numeric_data?.misc?.longest_gap_days?.[1] || 0;

  const bestDayMonth =
    data?.numeric_data?.misc?.best_day_date?.split('-')?.[1] || '-';
  const bestDayDay =
    data?.numeric_data?.misc?.best_day_date?.split('-')?.[2] || '-';
  const bestDayYear =
    data?.numeric_data?.misc?.best_day_date?.split('-')?.[0] || '-';

  return (
    <div className="container px-2 lg:px-4 xl:px-16 py-2 lg:py-4 mx-auto">
      <div className="h-full w-full flex flex-row flex-wrap justify-center items-center">
        <WrappedSection useTitle={false}>
          <div className="w-full h-auto flex flex-row flex-wrap -mb-4">
            <Link to="/wrapped">
              <LeftArrowIcon className="absolute ml-2 mt-2 h-8 w-8 text-gray-500 hover:text-gray-800" />
            </Link>
            <p className="text-xl font-semibold text-center w-full">
              {`${userId}'s`}
            </p>
            <p className="text-3xl text-center w-full">
              {`${year} GitHub Wrapped`}
            </p>
            <p className="mt-2 text-md text-center w-full text-gray-600">
              Private Access:{' '}
              {userId === currUserId && usePrivate ? 'True' : 'False'}
            </p>
            {data?.incomplete && (
              <p className="mt-2 text-md text-center w-full text-red-600">
                Incomplete Data. Please refresh later to finish loading.
              </p>
            )}
          </div>
        </WrappedSection>
        <WrappedSection title="Contribution Calendar">
          <div className="w-full lg:w-4/5">
            <Calendar
              data={data}
              startDate={`${year}-01-02`}
              endDate={`${parseInt(year) + 1}-01-01`}
              highlightDays={highlightDays}
              highlightColors={highlightColors}
            />
          </div>
          <div className="w-1/2 md:w-1/4 lg:w-1/5">
            <NumericOutOf
              num={data?.numeric_data?.misc?.total_days || 0}
              outOf={365}
              label="Active Days"
            />
          </div>
          <div className="w-1/2 md:w-1/4">
            <NumericOutOf
              num={data?.numeric_data?.misc?.longest_streak || 0}
              outOf={100}
              label="Longest Streak"
              className="hover:bg-gray-200 cursor-pointer"
              onMouseOver={() => {
                setHighlightDays(
                  Array.from(
                    { length: endStreak - startStreak + 1 },
                    (_, i) => startStreak + i,
                  ),
                );
              }}
              onMouseOut={() => {
                setHighlightDays([]);
              }}
            />
          </div>
          <div className="w-1/2 md:w-1/4">
            <NumericOutOf
              num={data?.numeric_data?.misc?.longest_gap || 0}
              outOf={100}
              label="Longest Gap"
              color="#EF4444"
              className="hover:bg-gray-200 cursor-pointer"
              onMouseOver={() =>
                setHighlightDays(
                  Array.from(
                    { length: endGap - startGap + 1 },
                    (_, i) => startGap + i,
                  ),
                )
              }
              onMouseOut={() => setHighlightDays([])}
            />
          </div>
          <div className="w-1/2 md:w-1/4">
            <NumericOutOf
              num={data?.numeric_data?.misc?.weekend_percent}
              outOf={100}
              format={(x) => `${x}%`}
              label="Weekend Activity"
              color="#468CBF"
              className="hover:bg-gray-200 cursor-pointer"
              onMouseOver={() => {
                const Sunday = Array.from({ length: 55 }, (_, i) => i).map(
                  (x) =>
                    x * 7 -
                    ((year % 7) + 6) +
                    Math.max(0, Math.floor((2024 - year) / 4)),
                );
                const Saturday = Array.from({ length: 55 }, (_, i) => i).map(
                  (x) =>
                    x * 7 -
                    (year % 7) +
                    Math.max(0, Math.floor((2024 - year) / 4)),
                );
                setHighlightDays([...Sunday, ...Saturday]);
              }}
              onMouseOut={() => setHighlightDays([])}
            />
          </div>
          <div className="hidden lg:block w-1/4">
            <NumericBestDay
              num={data?.numeric_data?.misc?.best_day_count}
              date={`${bestDayMonth}/${bestDayDay}/${bestDayYear}`}
              label="Busiest Day"
              className="hover:bg-gray-200 cursor-pointer"
              onMouseOver={() => {
                setHighlightColors(singleHoverScale);
                setHighlightDays([data?.numeric_data?.misc?.best_day_index]);
              }}
              onMouseOut={() => {
                setHighlightColors(hoverScale);
                setHighlightDays([]);
              }}
            />
          </div>
        </WrappedSection>
        <WrappedSection title="Lines of Code (LOC) Analysis">
          <div className="w-full md:w-1/2 xl:w-1/3">
            <PieLangs data={data} />
          </div>
          <div className="w-full md:w-1/2 xl:w-1/3">
            <PieRepos data={data} />
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
                label="Lines Changed / Day"
              />
            </div>
          </div>
        </WrappedSection>
        <WrappedSection title="Contribution Breakdown">
          <div className="w-full lg:w-1/3">
            <Radar data={data} />
          </div>
          <div className="w-full lg:w-2/3">
            <BarMonth data={data} />
          </div>
          <div className="w-full lg:w-2/3">
            <BarDay data={data} />
          </div>
          <div className="w-full lg:w-1/3">
            <SwarmDay data={data} />
          </div>
        </WrappedSection>
      </div>
      <FloatingIcon />
    </div>
  );
};

export default WrappedScreen;
