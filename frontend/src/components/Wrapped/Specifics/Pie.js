/* eslint-disable react/jsx-curly-newline */

import React from 'react';
import PropTypes from 'prop-types';

import { PieChart } from '../Templates';
import { WrappedCard } from '../Organization';

const PieLangs = ({ data, downloadLoading }) => {
  const [useLOCAdded, setUseLOCAdded] = React.useState(false);

  const metric = useLOCAdded ? 'added' : 'changed';
  const newData = data?.lang_data?.[`langs_${metric}`] || [];

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <div className="flex">
          <div className="flex-grow">
            <p className="text-xl font-semibold">Most Used Languages</p>
            <p>{useLOCAdded ? 'By LOC Added' : 'By LOC Changed'}</p>
          </div>
          {!downloadLoading && (
            <div className="flex-shrink-0">
              <button
                type="button"
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={() => setUseLOCAdded(!useLOCAdded)}
              >
                <span>Toggle</span>
              </button>
            </div>
          )}
        </div>
        <PieChart
          data={newData}
          getArcLinkLabel={(e) => e.data.label}
          getFormattedValue={(e) => e.formatted_value}
          colors={{ datum: 'data.color' }}
        />
      </WrappedCard>
    </div>
  );
};

PieLangs.propTypes = {
  data: PropTypes.object.isRequired,
  downloadLoading: PropTypes.bool.isRequired,
};

const PieRepos = ({ data, downloadLoading }) => {
  const [useLOCAdded, setUseLOCAdded] = React.useState(false);

  const metric = useLOCAdded ? 'added' : 'changed';
  const newData = data?.repo_data?.[`repos_${metric}`] || [];

  return (
    <div className="h-96 w-full">
      <WrappedCard>
        <div className="flex">
          <div className="flex-grow">
            <p className="text-xl font-semibold">Most Active Repositories</p>
            <p>{useLOCAdded ? 'By LOC Added' : 'By LOC Changed'}</p>
          </div>
          {!downloadLoading && (
            <div className="flex-shrink-0">
              <button
                type="button"
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={() => setUseLOCAdded(!useLOCAdded)}
              >
                <span>Toggle</span>
              </button>
            </div>
          )}
        </div>
        <PieChart
          data={newData}
          getArcLinkLabel={({ data: { label } }) => {
            if (label && label.includes('/')) {
              return label.split('/')[1].replace('repository', 'private');
            }
            return label;
          }}
          getFormattedValue={(e) => e.formatted_value}
          colors={{ scheme: 'category10' }}
        />
      </WrappedCard>
    </div>
  );
};

PieRepos.propTypes = {
  data: PropTypes.object.isRequired,
  downloadLoading: PropTypes.bool.isRequired,
};

export { PieLangs, PieRepos };
