/* eslint-disable jsx-a11y/anchor-is-valid */

import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import {
  BrowserRouter as Router,
  Routes,
  Route,
  useParams,
} from 'react-router-dom';

import Header from './Header';
import LandingScreen from '../Landing';
import DemoScreen from '../Demo';
import { SignUpScreen } from '../Auth';
import HomeScreen from '../Home';
import SettingsScreen from '../Settings';
import { NoMatchScreen, RedirectScreen } from '../Misc';

import { setPrivateAccess as _setPrivateAccess } from '../../redux/actions/userActions';
import { getUserMetadata } from '../../api';
import { WRAPPED_URL } from '../../constants';
import Footer from './Footer';

function WrappedAuthRedirectScreen() {
  // for wrapped auth redirects
  const { rest } = useParams();
  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    window.location.href = `${WRAPPED_URL}/${rest}?code=${code}`;
  }, [rest]);

  return null;
}

function WrappedRedirectScreen() {
  // redirects /wrapped/* to https://www.githubwrapped.com/*
  const { userId, year } = useParams();
  useEffect(() => {
    if (userId) {
      if (year) {
        window.location.href = `${WRAPPED_URL}/${userId}/${year}`;
      } else {
        window.location.href = `${WRAPPED_URL}/${userId}`;
      }
    } else {
      window.location.href = `${WRAPPED_URL}/`;
    }
  }, [userId, year]);
}

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
        <Header mode="trends" />
        <section className="bg-white text-gray-700 flex-grow">
          <Routes>
            {!isAuthenticated && (
              <Route path="/signup" element={<SignUpScreen />} />
            )}
            <Route path="/demo" element={<DemoScreen />} />
            <Route path="/user/redirect" element={<RedirectScreen />} />
            <Route
              path="/user/wrapped/:rest"
              element={<WrappedAuthRedirectScreen />}
            />
            <Route path="/user/*" element={<HomeScreen />} />
            <Route
              path="/wrapped/:userId/:year"
              element={<WrappedRedirectScreen />}
            />
            <Route
              path="/wrapped/:userId"
              element={<WrappedRedirectScreen />}
            />
            <Route path="/wrapped" element={<WrappedRedirectScreen />} />
            <Route path="/settings" element={<SettingsScreen />} />
            <Route path="/:userId" element={<WrappedRedirectScreen />} />
            <Route exact path="/" element={<LandingScreen />} />
            <Route path="*" element={<NoMatchScreen />} />
          </Routes>
        </section>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
