/* eslint-disable jsx-a11y/anchor-is-valid */

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import LandingScreen from '../Landing';
import { LoginScreen, SignUpScreen } from '../Auth';
import HomeScreen from '../Home';

import { logout as _logout } from '../../redux/actions/userActions';
import { PROD, CLIENT_ID, REDIRECT_URI } from '../../constants';

import { LightningSVG } from '../../assets';

function App() {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const logout = () => dispatch(_logout());

  console.log(PROD, CLIENT_ID, REDIRECT_URI);

  return (
    <div className="h-screen flex flex-col">
      <Router>
        <div className="text-gray-100 bg-white shadow-md body-font sticky top-0">
          <div className="container mx-auto flex flex-wrap p-5 flex-row items-center">
            <a className="title-font font-medium text-gray-700 mb-0">
              <Link to="/" className="flex items-center">
                <LightningSVG />
                <span className="ml-3 text-xl">GitHub Trends</span>
              </Link>
            </a>
            <nav className="ml-auto flex flex-wrap items-center text-base justify-center">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/"
                    className="px-4 py-1 mr-3 rounded text-gray-700 hover:bg-gray-300"
                    onClick={logout}
                  >
                    Sign Out
                  </Link>
                  <Link
                    to="/user"
                    className="px-4 py-1 mr-3 rounded bg-blue-500 hover:bg-blue-700 hover:text-gray-300"
                  >
                    Dashboard
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-4 py-1 mr-3 rounded text-gray-700 hover:bg-gray-300"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="px-4 py-1 mr-3 rounded bg-blue-500 hover:bg-blue-700 hover:text-gray-300"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </nav>
          </div>
        </div>
        <section className="flex-grow">
          <Switch>
            <Route path="/login" component={LoginScreen} />
            <Route path="/signup" component={SignUpScreen} />
            <Route path="/user" component={HomeScreen} />
            <Route path="/" component={LandingScreen} />
          </Switch>
        </section>
        <footer className="body-font">
          <div className="bg-gray-100">
            <div className="container mx-auto py-4 px-5">
              <p className="text-gray-500 text-sm text-center">
                © 2021 GitHub Trends
              </p>
            </div>
          </div>
        </footer>
      </Router>
    </div>
  );
}

export default App;
