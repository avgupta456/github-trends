/* eslint-disable jsx-a11y/anchor-is-valid */

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import LandingScreen from '../Landing';
import DemoScreen from '../Demo';
import { LoginScreen, SignUpScreen } from '../Auth';
import HomeScreen from '../Home';
import CustomizeScreen from '../Customize';
import { NoMatchScreen, RedirectScreen } from '../Misc';

import { logout as _logout } from '../../redux/actions/userActions';

import { HamburgerMenu, LightningSVG } from '../../assets';

function App() {
  const userId = useSelector((state) => state.user.userId);

  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();

  const logout = () => dispatch(_logout());

  const [toggle, setToggle] = React.useState(false);

  const toggleNav = () => {
    setToggle(!toggle);
  };

  return (
    <div className="h-screen flex flex-col">
      <Router>
        <div className="text-gray-100 bg-white shadow-md body-font sticky top-0 z-50">
          <div className="container mx-auto flex flex-wrap p-5 flex-row items-center">
            <nav className="bg-white w-full">
              <div className="mx-auto px-4">
                <div className="flex justify-between">
                  <div className="flex space-x-7">
                    <div>
                      <Link
                        to="/"
                        className="flex items-center title-font font-medium text-gray-700 mb-0 mr-8"
                      >
                        <LightningSVG />
                        <span className="ml-3 text-xl">GitHub Trends</span>
                      </Link>
                    </div>
                    <div className="hidden md:flex items-center space-x-1">
                      {isAuthenticated ? (
                        <Link
                          to="/user"
                          className="px-4 py-1 mr-3 rounded bg-gray-100 hover:bg-gray-300 text-gray-700"
                        >
                          Dashboard
                        </Link>
                      ) : (
                        <Link
                          to="/demo"
                          className="px-4 py-1 mr-3 rounded bg-gray-100 hover:bg-gray-300 text-gray-700"
                        >
                          Demo
                        </Link>
                      )}
                    </div>
                  </div>
                  <div className="hidden md:flex items-center space-x-3 ">
                    {isAuthenticated ? (
                      <>
                        <Link
                          to="/"
                          className="px-4 py-1 mr-3 rounded text-gray-700 bg-gray-100 hover:bg-gray-300"
                          onClick={logout}
                        >
                          Sign Out
                        </Link>
                      </>
                    ) : (
                      <>
                        <Link
                          to="/login"
                          className="px-4 py-1 mr-3 rounded text-gray-700 bg-gray-100 hover:bg-gray-300"
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
                  </div>
                  <div className="md:hidden flex items-center">
                    <button
                      type="button"
                      className="outline-none mobile-menu-button"
                      onClick={toggleNav}
                    >
                      <HamburgerMenu />
                    </button>
                  </div>
                </div>
                <div
                  className={`${
                    toggle ? ' mobile-menu' : 'hidden mobile-menu'
                  }`}
                >
                  <ul className="">
                    {isAuthenticated ? (
                      <li>
                        <Link
                          to="/user"
                          className="block text-sm px-2 py-4 text-gray-500 hover:text-gray-700 transition duration-300"
                        >
                          Dashboard
                        </Link>
                      </li>
                    ) : (
                      <li>
                        <Link
                          to="/demo"
                          className="block text-sm px-2 py-4 text-gray-500 hover:text-gray-700 transition duration-300"
                        >
                          Demo
                        </Link>
                      </li>
                    )}

                    {isAuthenticated ? (
                      <>
                        <Link
                          to="/"
                          className="block text-sm px-2 py-4 rounded text-gray-700 bg-gray-100 hover:bg-gray-300"
                          onClick={logout}
                        >
                          Sign Out
                        </Link>
                      </>
                    ) : (
                      <>
                        <li>
                          <Link
                            to="/login"
                            className="block text-sm rounded px-2 bg-gray-100 py-4 text-gray-700 hover:bg-gray-300 transition duration-300"
                          >
                            Login
                          </Link>
                        </li>
                        <li>
                          <Link
                            to="/signup"
                            className="block text-sm px-2 py-4  rounded bg-blue-500 hover:bg-blue-700 hover:text-gray-300"
                          >
                            Sign Up
                          </Link>
                        </li>
                      </>
                    )}
                  </ul>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <section className="flex-grow">
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
