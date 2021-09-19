/* eslint-disable react/button-has-type */
/* eslint-disable jsx-a11y/anchor-is-valid */

import React from 'react';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import HomeScreen from '../Home';
import LoginScreen from '../Auth';
import { LightningSVG } from '../../assets';

function App() {
  return (
    <Router>
      <header className="text-gray-100 body-font bg-blue-500 w-screen fixed">
        <div className="container mx-auto flex flex-wrap p-5 flex-row items-center">
          <a className="flex title-font font-medium items-center text-gray-100 mb-0">
            <LightningSVG />
            <span className="ml-3 text-xl">GitHub Trends</span>
          </a>
          <nav className="ml-auto flex flex-wrap items-center text-base justify-center">
            <Link to="/login" className="mr-5 hover:text-gray-300">
              Login
            </Link>
            <Link to="/" className="mr-5 hover:text-gray-300">
              Home
            </Link>
          </nav>
        </div>
      </header>
      <br />
      <br />
      <br />
      <Switch>
        <Route path="/login" component={LoginScreen} />
        <Route path="/" component={HomeScreen} />
      </Switch>
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
  );
}

export default App;
