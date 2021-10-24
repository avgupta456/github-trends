/* eslint-disable jsx-a11y/anchor-is-valid */

import React from 'react';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import Header from './Header';
import LandingScreen from '../Landing';
import DemoScreen from '../Demo';
import { LoginScreen, SignUpScreen } from '../Auth';
import HomeScreen from '../Home';
import CustomizeScreen from '../Customize';
import { NoMatchScreen, RedirectScreen } from '../Misc';

function App() {
  return (
    <div className="h-screen flex flex-col">
      <Router>
        <Header />
        <section className="bg-white text-gray-700 flex-grow">
          <Switch>
            <Route path="/login" component={LoginScreen} />
            <Route path="/signup" component={SignUpScreen} />
            <Route path="/demo" component={DemoScreen} />
            <Route path="/user/redirect" component={RedirectScreen} />
            <Route path="/user" component={HomeScreen} />
            <Route path="/customize/:suffix" component={CustomizeScreen} />
            <Route exact path="/" component={LandingScreen} />
            <Route path="*" component={NoMatchScreen} />
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
