import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

import { getWrapped } from '../../api';
import { Calendar } from '../../components';

const WrappedScreen = () => {
  const userId = useSelector((state) => state.user.userId);
  // eslint-disable-next-line no-unused-vars
  const [year, setYear] = useState(2021);

  const [data, setData] = useState({});

  useEffect(async () => {
    if (userId.length > 0 && year > 2010 && year <= 2021) {
      setData(await getWrapped(userId, year));
    }
  }, [userId, year]);

  console.log(userId, year, data);

  return (
    <div className="h-full w-full flex flex-col justify-center items-center">
      <Calendar
        startDate="2021-01-02"
        endDate="2021-12-31"
        data={data.calendar_data}
      />
    </div>
  );
};

export default WrappedScreen;
