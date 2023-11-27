/* eslint-disable jsx-a11y/anchor-is-valid */

import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Header from './Header';
import { SignUpScreen } from '../Auth';
import { SelectUserScreen, WrappedScreen } from '../Wrapped';
import { NoMatchScreen } from '../Misc';

import { setPrivateAccess as _setPrivateAccess } from '../../redux/actions/userActions';
import { getUserMetadata } from '../../api';
import Footer from './Footer';

function App() {
  const userId = useSelector((state) => state.user.userId);
  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();
  const setPrivateAccess = (access) => dispatch(_setPrivateAccess(access));

  useEffect(() => {
    async function getPrivateAccess() {
      if (userId && userId.length > 0) {
        const result = await getUserMetadata(userId);
        if (result !== null && result.private_access !== undefined) {
          setPrivateAccess(result.private_access);
        }
      }
    }
    getPrivateAccess();
  }, [userId]);

  return (
    <div className="h-screen flex flex-col">
      <Router>
        <Header mode="wrapped" />
        <section className="bg-white text-gray-700 flex-grow">
          <Routes>
            {!isAuthenticated && (
              <Route path="/signup" element={<SignUpScreen />} />
            )}
            <Route path="/" element={<SelectUserScreen />} />
            <Route path="/public/" element={<SelectUserScreen />} />
            <Route path="/private/" element={<SelectUserScreen />} />
            <Route path="/:userId/:year" element={<WrappedScreen />} />
            <Route path="/:userId" element={<WrappedScreen />} />
            <Route path="*" element={<NoMatchScreen />} />
          </Routes>
        </section>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
