import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';

import { getWrapped } from '../../api';
import { BarGraph, Calendar, PieChart, SwarmPlot } from '../../components';

const WrappedScreen = () => {
  // eslint-disable-next-line prefer-const
  let { userId, year } = useParams();
  year = year || 2021;

  const [data, setData] = useState({});

  useEffect(async () => {
    if (
      userId.length > 0 &&
      year > 2010 &&
      year <= 2021 &&
      (data === null || data === undefined || Object.keys(data).length === 0)
    ) {
      setData(await getWrapped(userId, year));
    }
  }, [userId, year, data]);

  console.log(userId, year, data);

  if (data === undefined || data === null || Object.keys(data).length === 0) {
    return (
      <div className="w-3/4 mx-auto">
        <h1 className="text-center">Loading...</h1>
      </div>
    );
  }

  return (
    <div className="w-3/4 mx-auto">
      <div className="h-full w-full flex flex-col justify-center items-center">
        <Calendar
          startDate={`${year}-01-02`}
          endDate={`${year}-12-31`}
          data={data.calendar_data}
        />
        <div className="flex w-full">
          <PieChart data={data.pie_data} type="repos_added" usePrivate />
          <PieChart data={data.pie_data} type="langs_added" usePrivate />
        </div>
        <SwarmPlot data={data.swarm_data} type="type" usePrivate />
        <SwarmPlot data={data.swarm_data} type="weekday" usePrivate />
        <BarGraph data={data.bar_data} type="loc_changed" usePrivate />
      </div>
    </div>
  );
};

export default WrappedScreen;
