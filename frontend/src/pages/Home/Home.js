/* eslint-disable no-unused-vars */
/* eslint-disable react/no-array-index-key */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { useHistory } from 'react-router-dom';

import BounceLoader from 'react-spinners/BounceLoader';
import { FaGithub as GithubIcon } from 'react-icons/fa';

import { ProgressBar } from '../../components';
import { SelectCardStage, CustomizeStage, ThemeStage } from './stages';

import { setUserKey, authenticate } from '../../api';
import { login as _login } from '../../redux/actions/userActions';
import { PROD } from '../../constants';

const FloatingIcon = () => {
  return (
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
  );
};

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
  const [fullSuffix, setFullSuffix] = useState('');

  // for stage three
  const [themeSuffix, setThemeSuffix] = useState('');

  console.log(themeSuffix);

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
            <SelectCardStage
              selectedCard={selectedCard}
              setSelectedCard={setSelectedCard}
              setStage={setStage}
            />
          )}
          {stage === 1 && (
            <CustomizeStage
              selectedCard={selectedCard}
              setFullSuffix={setFullSuffix}
            />
          )}
          {stage === 2 && (
            <ThemeStage
              fullSuffix={fullSuffix}
              setThemeSuffix={setThemeSuffix}
            />
          )}
        </div>
      </div>
      <FloatingIcon />
    </div>
  );
};

export default HomeScreen;
