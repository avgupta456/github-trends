import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
// import IconButton from '@material-ui/core/IconButton';
// import MenuIcon from '@material-ui/icons/Menu';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <Router>
      <div className={classes.root}>

        <AppBar position="static">
          <Toolbar>
            {/*
          <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          */}
            <Typography variant="h6" className={classes.title}>
              GitHub Trends
            </Typography>
            <Button color="inherit" component={Link} to="/user">User</Button>
            <Button color="inherit" component={Link} to="/octoverse">Octoverse</Button>
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

function User() {
  return <h2>User</h2>;
}

function Octoverse() {
  return <h2>Octoverse</h2>;
}
