import React from 'react';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import HomeScreen from '../Home';
import LoginScreen from '../Auth';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={LoginScreen} />
        <Route path="/" component={HomeScreen} />
      </Switch>
    </Router>
  );
}

export default App;
