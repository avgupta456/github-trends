import React from 'react';
import PropTypes from 'prop-types';

import { Image, DateRangeSection, CheckboxSection } from '../../../components';

const CustomizeStage = ({
  selectedCard,
  selectedTimeRange,
  setSelectedTimeRange,
  usePrivate,
  setUsePrivate,
  groupOther,
  setGroupOther,
  groupPrivate,
  setGroupPrivate,
  privateAccess,
  useCompact,
  setUseCompact,
  usePercent,
  setUsePercent,
  useLocChanged,
  setUseLocChanged,
  fullSuffix,
}) => {
  return (
    <div className="w-full flex flex-wrap">
      <div className="h-auto lg:w-2/5 md:w-1/2 pr-10 p-10 rounded-sm bg-gray-200">
        <DateRangeSection
          selectedTimeRange={selectedTimeRange}
          setSelectedTimeRange={setSelectedTimeRange}
          privateAccess={privateAccess}
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
          disabled={!privateAccess}
        />
        {selectedCard === 'repos' && (
          <CheckboxSection
            title="Group Other Repositories?"
            text="Group all remaining repositories together at the bottom of the card."
            question="Group other repositories?"
            variable={groupOther}
            setVariable={setGroupOther}
          />
        )}
        {selectedCard === 'repos' && usePrivate && groupOther && (
          <CheckboxSection
            title="Group Private Repositories?"
            text="Force private repositories together at the bottom of the card."
            question="Group private commits?"
            variable={groupPrivate}
            setVariable={setGroupPrivate}
          />
        )}
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
  selectedTimeRange: PropTypes.object.isRequired,
  setSelectedTimeRange: PropTypes.func.isRequired,
  usePrivate: PropTypes.bool.isRequired,
  setUsePrivate: PropTypes.func.isRequired,
  groupOther: PropTypes.bool.isRequired,
  setGroupOther: PropTypes.func.isRequired,
  groupPrivate: PropTypes.bool.isRequired,
  setGroupPrivate: PropTypes.func.isRequired,
  privateAccess: PropTypes.bool.isRequired,
  useCompact: PropTypes.bool.isRequired,
  setUseCompact: PropTypes.func.isRequired,
  usePercent: PropTypes.bool.isRequired,
  setUsePercent: PropTypes.func.isRequired,
  useLocChanged: PropTypes.bool.isRequired,
  setUseLocChanged: PropTypes.func.isRequired,
  fullSuffix: PropTypes.string.isRequired,
};

export default CustomizeStage;
