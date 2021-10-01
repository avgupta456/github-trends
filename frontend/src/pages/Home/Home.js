/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import BounceLoader from 'react-spinners/BounceLoader';

import { Card } from '../../components';

import { BACKEND_URL } from '../../constants';
import { getAccessToken } from '../../api';
import { login as _login } from '../../redux/actions/userActions';

const HomeScreen = () => {
  const [isLoading, setIsLoading] = useState(false);

  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const login = (newUserId) => dispatch(_login(newUserId));

  console.log(isLoading, userId);

  useEffect(async () => {
    // After requesting Github access, Github redirects back to your app with a code parameter
    const url = window.location.href;
    const hasCode = url.includes('?code=');

    // If Github API returns the code parameter
    if (hasCode) {
      const newUrl = url.split('?code=');
      window.history.pushState({}, null, newUrl[0]);
      setIsLoading(true);
      const result = await getAccessToken(newUrl[1]);
      login(result);
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

  return (
    <div className="h-full py-8 px-8 text-gray-600 body-font">
      <div className="flex flex-col">
        <div className="h-1 bg-gray-200 rounded overflow-hidden">
          <div className="w-24 h-full bg-blue-500" />
        </div>
        <div className="flex flex-wrap sm:flex-row flex-col py-6 mb-12">
          <h1 className="sm:w-2/5 text-gray-900 font-medium title-font text-2xl mb-2 sm:mb-0">
            GitHub README SVG Gallery
          </h1>
          <p className="sm:w-3/5 leading-relaxed text-base sm:pl-10 pl-0">
            Scroll through the list of images and see which ones you like.
            Simply click on the image to copy the embeddable link. Each image
            can be customized via the edit button. Enjoy!
          </p>
        </div>
      </div>
      <div className="flex flex-wrap -mt-8">
        <div className="p-2 md:w-1/3 sm:mb-0 mb-6">
          <Card
            title="Language Contributions - Percent"
            description="See your language breakdown based on your commits, across all repositories you contribute to, not just ones you own."
            imageSrc={`${BACKEND_URL}/user/${userId}/svg/langs`}
          />
        </div>
        <div className="p-2 md:w-1/3 sm:mb-0 mb-6">
          <Card
            title="Language Contributions - Lines"
            description="See your language breakdown based on your commits, across all repositories you contribute to, not just ones you own."
            imageSrc={`${BACKEND_URL}/user/${userId}/svg/langs?use_percent=False`}
          />
        </div>
        <div className="p-2 md:w-1/3 sm:mb-0 mb-6">
          <Card
            title="Repository Contributions - Lines"
            description="See your repository breakdown based on total lines, separated by language."
            imageSrc={`${BACKEND_URL}/user/${userId}/svg/repos`}
          />
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
