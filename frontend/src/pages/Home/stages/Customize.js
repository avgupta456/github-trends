import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import { Image, DateRangeSection, CheckboxSection } from '../../../components';

const CustomizeStage = ({ selectedCard, setFullSuffix }) => {
  const defaultTimeRange = {
    id: 3,
    name: 'Past 1 Year',
    disabled: false,
    timeRange: 'one_year',
  };
  const [selectedTimeRange, setSelectedTimeRange] = useState(defaultTimeRange);

  const [usePercent, setUsePercent] = useState(false);
  const [usePrivate, setUsePrivate] = useState(false);
  const [useLocChanged, setUseLocChanged] = useState(false);
  const [useCompact, setUseCompact] = useState(false);

  const resetCustomizations = () => {
    setSelectedTimeRange(defaultTimeRange);
    setUsePercent(false);
    setUsePrivate(false);
    setUseLocChanged(false);
    setUseCompact(false);
  };

  useEffect(() => {
    resetCustomizations();
  }, [selectedCard]);

  const time = selectedTimeRange.timeRange;
  let fullSuffix = `${selectedCard}?time_range=${time}`;

  if (usePercent) {
    fullSuffix += '&use_percent=True';
  }

  if (usePrivate) {
    fullSuffix += '&include_private=True';
  }

  if (useLocChanged) {
    fullSuffix += '&loc_metric=changed';
  }

  if (useCompact) {
    fullSuffix += '&compact=True';
  }

  useEffect(() => {
    setFullSuffix(fullSuffix);
  }, [fullSuffix]);

  return (
    <div className="w-full flex flex-wrap">
      <div className="h-auto lg:w-2/5 md:w-1/2 pr-10 p-10 rounded bg-gray-200">
        <DateRangeSection
          selectedTimeRange={selectedTimeRange}
          setSelectedTimeRange={setSelectedTimeRange}
        />
        {selectedCard === 'langs' && (
          <CheckboxSection
            title="Compact View"
            text="Use default view or compact view."
            question="Use compact view?"
            variable={useCompact}
            setVariable={setUseCompact}
          />
        )}
        <CheckboxSection
          title="Include Private Repositories?"
          text="By default, private commits are hidden. We will never reveal private repository information."
          question="Use private commits?"
          variable={usePrivate}
          setVariable={setUsePrivate}
        />
        {selectedCard === 'langs' && (
          <CheckboxSection
            title="Percent vs LOC"
            text="Use absolute LOC (default) or percent to rank your top repositories"
            question="Use percent?"
            variable={usePercent}
            setVariable={setUsePercent}
            disabled={useCompact}
          />
        )}
        <CheckboxSection
          title="LOC Metric"
          text="By default, LOC are measured as Added: (+) - (-). Alternatively, you can use Changed: (+) + (-)"
          question="Use LOC changed?"
          variable={useLocChanged}
          setVariable={setUseLocChanged}
          disabled={selectedCard === 'langs' && usePercent}
        />
      </div>
      <div className="w-full lg:w-3/5 md:w-1/2 object-center pt-5 md:pt-0 pl-0 md:pl-5 lg:pl-0">
        <div className="w-full lg:w-3/5 mx-auto h-full flex flex-col justify-center">
          <Image imageSrc={fullSuffix} compact={useCompact} />
        </div>
      </div>
    </div>
  );
};

CustomizeStage.propTypes = {
  selectedCard: PropTypes.string.isRequired,
  setFullSuffix: PropTypes.func.isRequired,
};

export default CustomizeStage;
