import React from 'react';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import HomeScreen from '../Home';
import AuthScreen from '../Auth';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={HomeScreen} />
        <Route path="/login" component={AuthScreen} />
      </Switch>
    </Router>
  );
}

export default App;
