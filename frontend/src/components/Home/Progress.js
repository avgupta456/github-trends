import React from 'react';
import PropTypes from 'prop-types';

import {
  FaArrowLeft as LeftArrowIcon,
  FaArrowRight as RightArrowIcon,
} from 'react-icons/fa';

import { classnames } from '../../utils';

const ProgressSection = ({ num, item, passed, onClick, clickDisabled }) => {
  return (
    <button
      className={classnames(
        'w-1/4 flex flex-col mx-2 p-2 border-t-4',
        passed ? 'border-blue-500' : 'border-gray-400',
        clickDisabled ? 'cursor-not-allowed' : 'cursor-pointer',
      )}
      type="button"
      onClick={onClick}
    >
      <div
        className={classnames(
          'text-lg font-bold',
          passed ? 'text-blue-500' : 'text-gray-400',
        )}
      >
        {`Step ${num + 1}`}
      </div>
      <div className={classnames(passed ? 'text-gray-700' : 'text-gray-400')}>
        {item}
      </div>
    </button>
  );
};

ProgressSection.propTypes = {
  num: PropTypes.number.isRequired,
  item: PropTypes.string.isRequired,
  passed: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  clickDisabled: PropTypes.bool.isRequired,
};

const ProgressBar = ({
  items,
  currItem,
  setCurrItem,
  leftDisabled,
  rightDisabled,
}) => {
  const fullLeftDisabled = leftDisabled || currItem === 0;
  const fullRightDisabled = rightDisabled || currItem === items.length - 1;

  return (
    <div className="w-full flex items-center">
      <LeftArrowIcon
        className={classnames(
          'w-8 h-8',
          fullLeftDisabled
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-gray-700 cursor-pointer',
        )}
        onClick={() => setCurrItem(currItem - 1)}
      />
      <div className="px-2 flex-grow flex flex-row">
        {items.map((item, index) => {
          return (
            <ProgressSection
              num={index}
              item={item}
              passed={currItem >= index}
              onClick={() => setCurrItem(index)}
              clickDisabled={
                (currItem > index && fullLeftDisabled) ||
                (currItem < index && fullRightDisabled)
              }
            />
          );
        })}
      </div>
      <RightArrowIcon
        className={classnames(
          'w-8 h-8',
          fullRightDisabled
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-gray-700 cursor-pointer',
        )}
        onClick={() => setCurrItem(currItem + 1)}
      />
    </div>
  );
};

ProgressBar.propTypes = {
  items: PropTypes.array.isRequired,
  currItem: PropTypes.number.isRequired,
  setCurrItem: PropTypes.func.isRequired,
  leftDisabled: PropTypes.bool,
  rightDisabled: PropTypes.bool,
};

ProgressBar.defaultProps = {
  leftDisabled: false,
  rightDisabled: false,
};

export default ProgressBar;
