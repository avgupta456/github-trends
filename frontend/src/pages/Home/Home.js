import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { useNavigate } from 'react-router-dom';
import BounceLoader from 'react-spinners/BounceLoader';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import { ProgressBar } from '../../components';
import {
  SelectCardStage,
  CustomizeStage,
  ThemeStage,
  DisplayStage,
} from './stages';

import { setUserKey, authenticate } from '../../api';
import { login as _login } from '../../redux/actions/userActions';
import { PROD } from '../../constants';

const HomeScreen = () => {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);

  const userId = useSelector((state) => state.user.userId);
  const privateAccess = useSelector((state) => state.user.privateAccess);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const login = (newUserId, userKey) => dispatch(_login(newUserId, userKey));

  // for all stages
  const [stage, setStage] = useState(0);

  // for stage one
  const [selectedCard, setSelectedCard] = useState('langs');

  // for stage two
  const defaultTimeRange = {
    id: 3,
    label: 'Past 1 Year',
    disabled: false,
    value: 'one_year',
  };
  const [selectedTimeRange, setSelectedTimeRange] = useState(defaultTimeRange);

  const [usePercent, setUsePercent] = useState(false);
  const [usePrivate, setUsePrivate] = useState(false);
  const [groupOther, setGroupOther] = useState(false);
  const [groupPrivate, setGroupPrivate] = useState(false);
  const [useLocChanged, setUseLocChanged] = useState(false);
  const [useCompact, setUseCompact] = useState(false);

  const resetCustomization = () => {
    setSelectedTimeRange(defaultTimeRange);
    setUsePercent(false);
    setUsePrivate(false);
    setUseLocChanged(false);
    setUseCompact(false);
  };

  useEffect(() => {
    resetCustomization();
  }, [selectedCard]);

  const time = selectedTimeRange.value;
  let fullSuffix = `${selectedCard}?time_range=${time}`;

  if (usePercent) {
    fullSuffix += '&use_percent=True';
  }

  if (usePrivate) {
    fullSuffix += '&include_private=True';
  }

  if (usePrivate && groupOther && groupPrivate) {
    fullSuffix += '&group=private';
  } else if (groupOther) {
    fullSuffix += '&group=other';
  }

  if (useLocChanged) {
    fullSuffix += '&loc_metric=changed';
  }

  if (useCompact) {
    fullSuffix += '&compact=True';
  }

  // for stage three
  const [theme, setTheme] = useState('classic');
  const themeSuffix = `${fullSuffix}&theme=${theme}`;

  useEffect(() => {
    async function redirectCode() {
      // After requesting Github access, Github redirects back to your app with a code parameter
      const url = window.location.href;

      if (url.includes('error=')) {
        navigate('/');
      }

      // If Github API returns the code parameter
      if (url.includes('code=')) {
        const tempPrivateAccess = url.includes('private');
        const newUrl = url.split('?code=');
        const subStr = PROD ? 'githubtrends.io' : 'localhost:3000';
        const redirect = `${url.split(subStr)[0]}${subStr}/user`;
        window.history.pushState({}, null, redirect);
        setIsLoading(true);
        const userKey = await setUserKey(newUrl[1]);
        const newUserId = await authenticate(newUrl[1], tempPrivateAccess);
        login(newUserId, userKey);
        setIsLoading(false);
      }
    }

    redirectCode();
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

  return (
    <div className="h-full px-2 py-4 lg:p-8 text-gray-600 body-font">
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
        />
        <div className="m-4 rounded-sm">
          <div className="lg:p-4">
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
            <SelectCardStage
              selectedCard={selectedCard}
              setSelectedCard={setSelectedCard}
            />
          )}
          {stage === 1 && (
            <CustomizeStage
              selectedCard={selectedCard}
              selectedTimeRange={selectedTimeRange}
              setSelectedTimeRange={setSelectedTimeRange}
              usePrivate={usePrivate}
              setUsePrivate={setUsePrivate}
              groupOther={groupOther}
              setGroupOther={setGroupOther}
              groupPrivate={groupPrivate}
              setGroupPrivate={setGroupPrivate}
              privateAccess={privateAccess}
              useCompact={useCompact}
              setUseCompact={setUseCompact}
              usePercent={usePercent}
              setUsePercent={setUsePercent}
              useLocChanged={useLocChanged}
              setUseLocChanged={setUseLocChanged}
              fullSuffix={fullSuffix}
            />
          )}
          {stage === 2 && (
            <ThemeStage
              theme={theme}
              setTheme={setTheme}
              fullSuffix={fullSuffix}
            />
          )}
          {stage === 3 && (
            <DisplayStage userId={userId} themeSuffix={themeSuffix} />
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
            className="rounded-sm shadow bg-gray-700 hover:bg-gray-800 text-gray-50 px-3 py-2 flex items-center"
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
