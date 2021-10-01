import React from 'react';
import { useSelector } from 'react-redux';

import { Image } from '../../components';
import { LightningSVG } from '../../assets/svgs';

import { BACKEND_URL } from '../../constants';

const Customize = () => {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

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

  const section = (
    <div className="flex relative pb-12">
      <div className="h-full w-10 absolute inset-0 flex items-center justify-center">
        <div className="h-full w-1 bg-gray-200 pointer-events-none" />
      </div>
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-500 inline-flex items-center justify-center text-white relative z-10">
        <LightningSVG />
      </div>
      <div className="flex-grow pl-4">
        <h2 className="font-medium title-font text-sm text-gray-900 mb-1 tracking-wider">
          STEP 1
        </h2>
        <p className="leading-relaxed">
          VHS cornhole pop-up, try-hard 8-bit iceland helvetica. Kinfolk bespoke
          try-hard cliche palo santo offal.
        </p>
      </div>
    </div>
  );

  return (
    <div className="h-full py-8 flex justify-center items-center text-gray-600 body-font">
      <div className="container px-8 mx-auto flex flex-wrap">
        <div className="w-full h-1 bg-gray-200 rounded overflow-hidden">
          <div className="w-48 h-full bg-blue-500" />
        </div>
        <div className="flex flex-wrap sm:flex-row flex-col py-6 mb-12">
          <h1 className="sm:w-2/5 text-gray-900 font-medium title-font text-2xl mb-2 sm:mb-0">
            Customize your SVG
          </h1>
          <p className="sm:w-3/5 leading-relaxed text-base sm:pl-10 pl-0">
            Modify the SVG to your liking. Edit the start and end date, exclude
            specific languages or repositories, control the theme, and more!
          </p>
        </div>
        <div className="lg:w-2/5 md:w-1/2 md:pr-10">
          {section}
          {section}
          {section}
          {section}
          {section}
        </div>
        <div className="lg:w-3/5 md:w-1/2 object-center bg-gray-50">
          <div className="w-3/5 mx-auto mt-16">
            <Image imageSrc={`${BACKEND_URL}/user/${userId}/svg/langs`} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Customize;
