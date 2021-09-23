import React from 'react';
import { useSelector } from 'react-redux';

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
  return (
    <div className="h-full py-8 flex justify-center items-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold">Work in Progress!</h1>
      </div>
    </div>
  );
};

export default Customize;
