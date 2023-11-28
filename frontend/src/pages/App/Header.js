import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';

import { Link } from 'react-router-dom';

import { GiHamburgerMenu as HamburgerIcon } from 'react-icons/gi';
import { MdSettings as SettingsIcon } from 'react-icons/md';

import { logout as _logout } from '../../redux/actions/userActions';
import rocketIcon from '../../assets/rocket.png';
import { classnames } from '../../utils';
import { GITHUB_PUBLIC_AUTH_URL, WRAPPED_URL } from '../../constants';

const propTypes = {
  to: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func,
  className: PropTypes.string,
};

const defaultProps = {
  onClick: null,
  className: null,
};

const StandardLink = ({ to, children, onClick, className }) => (
  <Link
    to={to}
    className={classnames(
      'px-4 py-1 mr-3 rounded-sm bg-gray-200 hover:bg-gray-300 text-gray-700',
      className,
    )}
    onClick={onClick}
  >
    {children}
  </Link>
);

StandardLink.propTypes = propTypes;

StandardLink.defaultProps = defaultProps;

const MobileLink = ({ to, children, onClick, className }) => (
  <Link
    to={to}
    className={classnames(
      'block text-sm px-2 my-2 py-2 rounded-sm bg-gray-200 text-gray-700',
      className,
    )}
    onClick={onClick}
  >
    {children}
  </Link>
);

MobileLink.propTypes = propTypes;

MobileLink.defaultProps = defaultProps;

const Header = ({ mode }) => {
  const [toggle, setToggle] = useState(false);

  const userId = useSelector((state) => state.user.userId);
  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();
  const logout = () => dispatch(_logout());

  return (
    <div className="text-gray-100 bg-white shadow-md body-font top-0 z-50">
      <div className="p-5 flex flex-wrap">
        {/* GitHub Trends Logo */}
        <Link
          to="/"
          className="flex items-center title-font font-medium text-gray-700 mb-0 md:mr-8"
        >
          <img src={rocketIcon} alt="logo" className="w-6 h-6" />
          {mode === 'trends' && (
            <span className="ml-2 text-xl">GitHub Trends</span>
          )}
          {mode === 'wrapped' && (
            <span className="ml-2 text-xl">GitHub Wrapped</span>
          )}
        </Link>
        {/* Pages: Wrapped, Dashboard, Demo */}
        {mode === 'trends' && (
          <div className="hidden md:flex">
            <Link
              to={WRAPPED_URL}
              className="px-4 py-1 mr-3 rounded-sm bg-blue-500 hover:bg-blue-600 text-white"
            >
              Wrapped
            </Link>
            {isAuthenticated ? (
              <StandardLink to="/user">Dashboard</StandardLink>
            ) : (
              <StandardLink to="/demo">Demo</StandardLink>
            )}
          </div>
        )}
        {/* Auth Pages: Sign Up, Log In, Log Out */}
        <div className="hidden md:flex ml-auto items-center text-base justify-center">
          {isAuthenticated ? (
            <>
              {mode === 'trends' && (
                <Link to="/settings" className="mr-3 px-1 py-1">
                  <SettingsIcon className="h-6 w-6 text-gray-700" />
                </Link>
              )}
              <StandardLink to="/" onClick={logout}>
                Sign Out
              </StandardLink>
            </>
          ) : (
            <>
              <a
                className="px-4 py-1 mr-3 rounded-sm bg-gray-200 hover:bg-gray-300 text-gray-700"
                href={GITHUB_PUBLIC_AUTH_URL}
              >
                Login
              </a>
              <Link
                to="/signup"
                className="px-4 py-1 mr-3 rounded-sm bg-blue-500 hover:bg-blue-700 hover:text-gray-300"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
        {/* Hamburger Menu */}
        <div className="md:hidden flex ml-auto items-center">
          <button
            type="button"
            className="outline-none"
            onClick={() => setToggle(!toggle)}
          >
            <HamburgerIcon className="w-6 h-6 text-gray-700" />
          </button>
        </div>
      </div>
      {/* Hamburger Dropdown */}
      <div className={classnames('p-5 pt-0', !toggle && 'hidden')}>
        {mode === 'trends' && (
          <>
            <MobileLink to={WRAPPED_URL} onClick={() => setToggle(false)}>
              Wrapped
            </MobileLink>
            {isAuthenticated ? (
              <MobileLink to="/user" onClick={() => setToggle(false)}>
                Dashboard
              </MobileLink>
            ) : (
              <MobileLink to="/demo" onClick={() => setToggle(false)}>
                Demo
              </MobileLink>
            )}
          </>
        )}
        {isAuthenticated ? (
          <>
            {mode === 'trends' && (
              <MobileLink to="/settings" onClick={() => setToggle(false)}>
                Settings
              </MobileLink>
            )}
            <MobileLink
              to="/"
              onClick={() => {
                setToggle(false);
                logout();
              }}
            >
              Sign Out
            </MobileLink>
          </>
        ) : (
          <>
            <a
              className="block text-sm px-2 my-2 py-2 rounded-sm bg-gray-200 text-gray-700"
              href={GITHUB_PUBLIC_AUTH_URL}
            >
              Login
            </a>
            <Link
              to="/signup"
              onClick={() => setToggle(false)}
              className="block text-sm px-2 my-2 py-2 rounded-sm bg-blue-500 text-white"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </div>
  );
};

Header.propTypes = {
  mode: PropTypes.string.isRequired,
};

export default Header;
