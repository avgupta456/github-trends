/* eslint-disable no-unused-vars */
/* eslint-disable react/no-array-index-key */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { useHistory } from 'react-router-dom';

import BounceLoader from 'react-spinners/BounceLoader';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import {
  Image,
  Card,
  ProgressBar,
  DateRangeSection,
  CheckboxSection,
} from '../../components';

import { setUserKey, authenticate } from '../../api';
import { login as _login } from '../../redux/actions/userActions';
import { PROD } from '../../constants';

const HomeScreen = () => {
  const history = useHistory();

  const [isLoading, setIsLoading] = useState(false);

  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const login = (newUserId, userKey) => dispatch(_login(newUserId, userKey));

  useEffect(async () => {
    // After requesting Github access, Github redirects back to your app with a code parameter
    const url = window.location.href;

    if (url.includes('error=')) {
      history.push('/');
    }

    // If Github API returns the code parameter
    if (url.includes('code=')) {
      const privateAccess = url.includes('private');
      const newUrl = url.split('?code=');
      const subStr = PROD ? 'githubtrends.io' : 'localhost:3000';
      const redirect = `${url.split(subStr)[0]}${subStr}/user`;
      window.history.pushState({}, null, redirect);
      setIsLoading(true);
      const userKey = await setUserKey(newUrl[1]);
      const newUserId = await authenticate(newUrl[1], privateAccess);
      login(newUserId, userKey);
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <BounceLoader color="#3B82F6" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            Please sign in to access this page
          </h1>
        </div>
      </div>
    );
  }

  // for all stages
  const [stage, setStage] = useState(0);

  // for stage one
  const [selectedCard, setSelectedCard] = useState(null);

  // for stage two
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

  console.log(fullSuffix);

  return (
    <div className="h-full py-8 px-8 text-gray-600 body-font">
      <div className="flex flex-col">
        <ProgressBar
          items={[
            'Select Card',
            'Modify Parameters',
            'Customize Theme',
            'Display Card',
          ]}
          currItem={stage}
          setCurrItem={setStage}
          rightDisabled={stage === 0 && selectedCard === null}
        />
        <div className="m-4 rounded-lg">
          <div className="p-4">
            <div className="text-2xl text-gray-600 font-semibold">
              {
                [
                  'Select a Card',
                  'Modify Card Parameters',
                  'Choose a Theme',
                  'Display your Card',
                ][stage]
              }
            </div>
            <div>
              {
                [
                  'You will be able to customize your card in future steps.',
                  'Change the date range, include private commits, and more!',
                  'Choose from one of our predefined themes (more coming soon!)',
                  'Display your card on GitHub, Twitter, or Linkedin',
                ][stage]
              }
            </div>
          </div>
          {stage === 0 && (
            <div className="flex flex-wrap">
              {[
                {
                  title: 'Language Contributions',
                  description: 'See your overall language breakdown',
                  imageSrc: 'langs',
                },
                {
                  title: 'Repository Contributions',
                  description:
                    'See your most contributed repository by lines of code',
                  imageSrc: 'repos',
                },
              ].map((card, index) => (
                <button
                  className="w-1/3 p-4"
                  key={index}
                  type="button"
                  onClick={() => {
                    if (selectedCard !== card.imageSrc) {
                      setSelectedCard(card.imageSrc);
                      setStage(1);
                    } else {
                      setSelectedCard(null);
                    }
                  }}
                >
                  <Card
                    title={card.title}
                    description={card.description}
                    imageSrc={card.imageSrc}
                    selected={selectedCard === card.imageSrc}
                  />
                </button>
              ))}
            </div>
          )}
          {stage === 1 && (
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
          )}
        </div>
      </div>
      <div className="fixed bottom-8 right-8">
        <a
          href="https://www.github.com/avgupta456/github-trends"
          target="_blank"
          rel="noopener noreferrer"
        >
          <button
            type="button"
            className="rounded-full bg-gray-700 hover:bg-gray-800 text-gray-50 px-3 py-2 flex items-center"
          >
            Star on
            <GithubIcon className="ml-1.5 w-5 h-5" />
          </button>
        </a>
      </div>
    </div>
  );
};

export default HomeScreen;
