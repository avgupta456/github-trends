/* eslint-disable react/jsx-one-expression-per-line */

import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

import { useParams, Link } from 'react-router-dom';
import { toPng } from 'html-to-image';
import download from 'downloadjs';
import { FaArrowLeft as LeftArrowIcon } from 'react-icons/fa';
import { BsImage as ImageIcon, BsInfoCircle } from 'react-icons/bs';
import Select from 'react-select';
import { ClipLoader } from 'react-spinners';

import { getWrapped } from '../../api';
import {
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
import { classnames } from '../../utils';
import { CURR_YEAR } from '../../constants';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || `${CURR_YEAR}`;

  const currUserId = useSelector((state) => state.user.userId);
  const usePrivate = useSelector((state) => state.user.privateAccess);

  const [data, setData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [highlightDays, setHighlightDays] = useState([]);
  const [highlightColors, setHighlightColors] = useState(hoverScale);

  const [downloadLoading, setDownloadLoading] = useState(false);

  // eslint-disable-next-line no-unused-vars
  const downloadImage = async () => {
    const dataUrl = await toPng(document.getElementById('screenshot-div'));
    download(dataUrl, 'github-wrapped.png');
  };

  useEffect(() => {
    async function getData() {
      if (userId?.length > 0 && year > 2010 && year <= CURR_YEAR) {
        const output = await getWrapped(userId, year);
        if (
          output !== null &&
          output !== undefined &&
          Object.keys(output).length > 0
        ) {
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
    <div className="containermx-auto">
      <div
        className={classnames(
          'h-full w-full bg-white flex flex-row flex-wrap justify-center items-center',
          'px-2 lg:px-4 xl:px-16 py-4 lg:py-8',
        )}
        id="screenshot-div"
      >
        <WrappedSection useTitle={false}>
          <div className="w-full h-auto flex flex-row flex-wrap -mb-4">
            {!downloadLoading && (
              <Link to="/">
                <LeftArrowIcon className="hidden md:block absolute ml-2 mt-2 h-8 w-8 text-gray-500 hover:text-gray-800" />
              </Link>
            )}
            <p className="text-xl font-semibold text-center w-full">
              {`${userId}'s`}
            </p>
            <div className="w-full flex justify-center items-center">
              <Select
                options={Array.from(
                  { length: 10 },
                  (_, i) => CURR_YEAR - i,
                ).map((x) => ({ value: x, label: x }))}
                value={{ value: year, label: year }}
                onChange={(e) => {
                  window.location.href = `/${userId}/${e.value}`;
                }}
              />
              <p className="text-2xl md:text-3xl ml-2">GitHub Wrapped</p>
            </div>
            <div className="mt-2 text-md text-center w-full text-gray-600 flex justify-center items-center">
              Private Access:{' '}
              {userId === currUserId && usePrivate ? 'True' : 'False'}
              {!(userId === currUserId && usePrivate) && (
                <div
                  className="hidden md:inline md:tooltip"
                  data-tip="For private access, create an account with GitHub Trends and authenticate with GitHub."
                >
                  <BsInfoCircle className="h-4 w-4 ml-2 text-gray-500 hover:text-gray-800 cursor-pointer" />
                </div>
              )}
            </div>
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
              endDate={`${year}-12-31`}
              highlightDays={highlightDays}
              highlightColors={highlightColors}
              downloadLoading={downloadLoading}
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
            <PieLangs data={data} downloadLoading={downloadLoading} />
          </div>
          <div className="w-full md:w-1/2 xl:w-1/3">
            <PieRepos data={data} downloadLoading={downloadLoading} />
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
            <BarMonth data={data} downloadLoading={downloadLoading} />
          </div>
          <div className="w-full lg:w-2/3">
            <BarDay data={data} downloadLoading={downloadLoading} />
          </div>
          <div className="w-full lg:w-1/3">
            <SwarmDay data={data} />
          </div>
        </WrappedSection>
        {downloadLoading && (
          <div className="text-center text-2xl md:text-3xl lg:text-4xl font-bold text-blue-500">
            Create your own at www.githubwrapped.io
          </div>
        )}
      </div>
      <div className="fixed bottom-2 right-2 md:bottom-4 md:right-4 lg:bottom-8 lg:right-8">
        <button
          type="button"
          className="rounded-sm shadow bg-gray-700 hover:bg-gray-800 text-gray-50 px-3 py-2"
          onClick={() => {
            setDownloadLoading(true);
            setTimeout(() => {
              downloadImage();
              setDownloadLoading(false);
            }, 10);
          }}
        >
          {downloadLoading ? (
            <div className="w-28 h-6 flex justify-center">
              <ClipLoader size={22} color="#fff" speedMultiplier={0.5} />
            </div>
          ) : (
            <div className="w-28 h-6 flex items-center">
              <p>Save Image</p>
              <ImageIcon className="ml-1.5 w-5 h-5" />
            </div>
          )}
        </button>
      </div>
    </div>
  );
};

export default WrappedScreen;
