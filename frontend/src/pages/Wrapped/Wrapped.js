import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';
import { BounceLoader } from 'react-spinners';

import { getWrapped } from '../../api';
import {
  Checkbox,
  BarGraph,
  Calendar,
  Numeric,
  PieChart,
  SwarmPlot,
} from '../../components';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || 2021;

  const [data, setData] = useState({});
  const isLoading =
    data === undefined || data === null || Object.keys(data).length === 0;

  useEffect(async () => {
    if (userId.length > 0 && year > 2010 && year <= 2021 && isLoading) {
      setData(await getWrapped(userId, year));
    }
  }, [userId, year, data]);

  // eslint-disable-next-line no-unused-vars
  const [usePrivate, setUsePrivate] = useState(false);

  let contribData = {};
  try {
    contribData = data.numeric_data.contribs;
  } catch (e) {
    // do nothing
  }

  console.log(contribData);

  if (isLoading) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <BounceLoader color="#3B82F6" />
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
            data={contribData}
            usePrivate={usePrivate}
            type={item.type}
            label={item.label}
          />
        ))}
        <Calendar
          data={data.calendar_data}
          startDate={`${year}-01-02`}
          endDate={`${year}-12-31`}
          usePrivate={usePrivate}
        />
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
