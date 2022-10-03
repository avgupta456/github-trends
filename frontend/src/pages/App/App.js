/* eslint-disable jsx-a11y/anchor-is-valid */

import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Header from './Header';
import LandingScreen from '../Landing';
import DemoScreen from '../Demo';
import { LoginScreen, SignUpScreen } from '../Auth';
import HomeScreen from '../Home';
import { SelectUserScreen, WrappedScreen } from '../Wrapped';
import SettingsScreen from '../Settings';
import { NoMatchScreen, RedirectScreen } from '../Misc';

import { setPrivateAccess as _setPrivateAccess } from '../../redux/actions/userActions';
import { getUserMetadata } from '../../api';

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
        <Header />
        <section className="bg-white text-gray-700 flex-grow">
          <Routes>
            {!isAuthenticated && (
              <Route path="/login" component={LoginScreen} />
            )}
            {!isAuthenticated && (
              <Route path="/signup" element={<SignUpScreen />} />
            )}
            <Route path="/demo" element={<DemoScreen />} />
            <Route path="/user/redirect" element={<RedirectScreen />} />
            <Route path="/user" element={<HomeScreen />} />
            <Route path="/wrapped/:userId/:year" element={<WrappedScreen />} />
            <Route path="/wrapped/:userId" element={<WrappedScreen />} />
            <Route path="/wrapped" element={<SelectUserScreen />} />
            {isAuthenticated && (
              <Route path="/settings" element={<SettingsScreen />} />
            )}
            <Route exact path="/" element={<LandingScreen />} />
            <Route path="*" element={<NoMatchScreen />} />
          </Routes>
        </section>
        <footer className="body-font">
          <div className="bg-gray-100 border-t border-gray-300">
            <div className="container mx-auto py-4 px-5">
              <p className="text-gray-500 text-sm text-center">
                © 2022 GitHub Trends
              </p>
            </div>
          </div>
        </footer>
      </Router>
    </div>
  );
}

export default App;
