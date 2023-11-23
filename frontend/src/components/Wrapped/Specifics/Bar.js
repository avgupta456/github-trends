import React, { useState } from 'react';
import PropTypes from 'prop-types';

import { WrappedCard } from '../Organization';
import { BarGraph } from '../Templates';

const monthNames = [
  'Jan',
  'Feb',
  'March',
  'April',
  'May',
  'June',
  'July',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

const dayNames = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];

const BarMonth = ({ data, downloadLoading }) => {
  const newData = data?.month_data?.months || [];

  // eslint-disable-next-line no-unused-vars
  const [displayContribs, setDisplayContribs] = useState(true);

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <div className="flex">
          <div className="flex-grow">
            <p className="text-xl font-semibold">Contributions by Month</p>
            <p>
              {displayContribs ? 'By Contribution Count' : 'By LOC Changed'}
            </p>
          </div>
          {!downloadLoading && (
            <div className="flex-shrink-0">
              <button
                type="button"
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={() => setDisplayContribs(!displayContribs)}
              >
                <span>Toggle</span>
              </button>
            </div>
          )}
        </div>
        {displayContribs ? (
          <BarGraph
            data={newData}
            labels={monthNames}
            xTitle="Month"
            type="contribs"
            getLabel={(d) => d.contribs}
            legendText="Contributions"
          />
        ) : (
          <BarGraph
            data={newData}
            labels={monthNames}
            xTitle="Month"
            type="loc_changed"
            getLabel={(d) => d.formatted_loc_changed.split(' ')[0]}
            legendText="LOC Changed"
          />
        )}
      </WrappedCard>
    </div>
  );
};

BarMonth.propTypes = {
  data: PropTypes.object.isRequired,
  downloadLoading: PropTypes.bool.isRequired,
};

const BarDay = ({ data, downloadLoading }) => {
  const newData = data?.day_data?.days || [];

  const [displayContribs, setDisplayContribs] = useState(true);

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <div className="flex">
          <div className="flex-grow">
            <p className="text-xl font-semibold">Contributions by Day</p>
            <p>
              {displayContribs ? 'By Contribution Count' : 'By LOC Changed'}
            </p>
          </div>
          {!downloadLoading && (
            <div className="flex-shrink-0">
              <button
                type="button"
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={() => setDisplayContribs(!displayContribs)}
              >
                <span>Toggle</span>
              </button>
            </div>
          )}
        </div>
        {displayContribs ? (
          <BarGraph
            data={newData}
            labels={dayNames}
            xTitle="Day"
            type="contribs"
            getLabel={(d) => d.contribs}
            legendText="Contributions"
          />
        ) : (
          <BarGraph
            data={newData}
            labels={dayNames}
            xTitle="Day"
            type="loc_changed"
            getLabel={(d) => d.formatted_loc_changed.split(' ')[0]}
            legendText="LOC Changed"
          />
        )}
      </WrappedCard>
    </div>
  );
};

BarDay.propTypes = {
  data: PropTypes.object.isRequired,
  downloadLoading: PropTypes.bool.isRequired,
};

export { BarMonth, BarDay };
