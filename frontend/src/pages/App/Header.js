import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { Link } from 'react-router-dom';

import { HiOutlineLightningBolt as LightningIcon } from 'react-icons/hi';
import { GiHamburgerMenu as HamburgerIcon } from 'react-icons/gi';

import { logout as _logout } from '../../redux/actions/userActions';
import { classnames } from '../../utils';

const Header = () => {
  const [toggle, setToggle] = useState(false);

  const userId = useSelector((state) => state.user.userId);
  const isAuthenticated = userId && userId.length > 0;

  const dispatch = useDispatch();
  const logout = () => dispatch(_logout());

  return (
    <div className="text-gray-100 bg-white shadow-md body-font sticky top-0 z-50">
      <div className="p-5 flex flex-wrap">
        {/* GitHub Trends Logo */}
        <Link
          to="/"
          className="flex items-center title-font font-medium text-gray-700 mb-0 md:mr-8"
        >
          <LightningIcon className="w-5 h-5" />
          <span className="ml-3 text-xl">GitHub Trends</span>
        </Link>
        {/* Pages: Dashboard, Demo */}
        <div className="hidden md:flex">
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
        {/* Auth Pages: Sign Up, Log In, Log Out */}
        <div className="hidden md:flex ml-auto items-center text-base justify-center">
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
        {isAuthenticated ? (
          <>
            <Link
              to="/user"
              onClick={() => setToggle(false)}
              className="block text-sm px-2 my-2 py-2 rounded bg-gray-100 text-gray-700"
            >
              Dashboard
            </Link>
            <Link
              to="/"
              onClick={() => {
                setToggle(false);
                logout();
              }}
              className="block text-sm px-2 my-2 py-2 rounded bg-gray-100 text-gray-700"
            >
              Sign Out
            </Link>
          </>
        ) : (
          <>
            <Link
              to="/demo"
              onClick={() => setToggle(false)}
              className="block text-sm px-2 my-2 py-2 rounded bg-gray-100 text-gray-700"
            >
              Demo
            </Link>
            <Link
              to="/login"
              onClick={() => setToggle(false)}
              className="block text-sm px-2 my-2 py-2 rounded bg-gray-100 text-gray-700"
            >
              Login
            </Link>
            <Link
              to="/signup"
              onClick={() => setToggle(false)}
              className="block text-sm px-2 my-2 py-2 rounded bg-blue-500 text-white"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </div>
  );
};

export default Header;
