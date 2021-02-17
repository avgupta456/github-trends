import React from 'react';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
// import IconButton from '@material-ui/core/IconButton';
// import MenuIcon from '@material-ui/icons/Menu';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import User from '../User';
import Octoverse from '../Octoverse';

class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Router>
        <div style={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              {/*
              <IconButton edge="start" style={{ marginRight: 16 }}>
                <MenuIcon />
              </IconButton>
              */}
              <Typography variant="h6" style={{ flexGrow: 1 }}>
                GitHub Trends
              </Typography>
              <Button color="inherit" component={Link} to="/user">
                User
              </Button>
              <Button color="inherit" component={Link} to="/octoverse">
                Octoverse
              </Button>
            </Toolbar>
          </AppBar>
        </div>

        <Switch>
          <Route path="/user">
            <User />
          </Route>
          <Route path="/octoverse">
            <Octoverse />
          </Route>
        </Switch>
      </Router>
    );
  }
}

export default App;
