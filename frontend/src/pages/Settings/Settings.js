/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */

import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux';

import { Button } from '../../components';
import { logout as _logout } from '../../redux/actions/userActions';
import { deleteAccount } from '../../api';
import { classnames } from '../../utils';
import { GITHUB_PRIVATE_AUTH_URL, CLIENT_ID } from '../../constants';

const SectionButton = ({ name, implemented, isSelected, setSelected }) => {
  return (
    <div
      className={classnames(
        'w-full py-3 px-3 hover:bg-gray-100 text-gray-700 text-lg cursor-pointer',
        isSelected &&
          'pl-2 bg-gray-100 cursor-default border-l-4 border-blue-500',
        !implemented && 'opacity-50 cursor-not-allowed',
      )}
      onClick={() => setSelected('accountTier')}
    >
      {name}
    </div>
  );
};

SectionButton.propTypes = {
  name: PropTypes.string.isRequired,
  implemented: PropTypes.bool,
  isSelected: PropTypes.bool.isRequired,
  setSelected: PropTypes.func.isRequired,
};

SectionButton.defaultProps = {
  implemented: true,
};

function useOutsideAlerter(ref, action) {
  useEffect(() => {
    /**
     * Alert if clicked on outside of element
     */
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        action();
      }
    }

    // Bind the event listener
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      // Unbind the event listener on clean up
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [ref]);
}

const SettingsScreen = () => {
  const [selected, setSelected] = useState('accountTier');
  const [deleteModal, setDeleteModal] = useState(false);

  const openDeleteModal = () => {
    setDeleteModal(true);
  };

  const closeDeleteModal = () => {
    setDeleteModal(false);
  };

  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef, closeDeleteModal);

  const userId = useSelector((state) => state.user.userId);
  const isAuthenticated = userId && userId.length > 0;
  const userKey = useSelector((state) => state.user.userKey);
  const privateAccess = useSelector((state) => state.user.privateAccess);
  const accountTier = privateAccess ? 'Private Workflow' : 'Public Workflow';

  const dispatch = useDispatch();
  const logout = () => dispatch(_logout());

  console.log(isAuthenticated, userId, userKey, privateAccess, accountTier);

  if (!isAuthenticated) {
    return (
      <div className="h-full py-8 flex justify-center items-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            Please sign in to access this page
          </h1>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full w-full">
      <div className={classnames('h-full flex', deleteModal && 'opacity-25')}>
        <div className="h-full w-1/3 md:w-80 p-4 flex flex-col border-r">
          <p className="p-2 text-gray-700 text-lg font-bold">
            Account Settings
          </p>
          <hr />
          <SectionButton
            name="Account Tier"
            isSelected={selected === 'accountTier'}
            setSelected={() => setSelected('accountTier')}
          />
          <SectionButton
            name="Personalization"
            implemented={false}
            isSelected={selected === 'personalization'}
            setSelected={() => setSelected('personalization')}
          />
          <SectionButton
            name="Delete Account"
            isSelected={selected === 'deleteAccount'}
            setSelected={() => setSelected('deleteAccount')}
          />
        </div>
        <div className="h-full w-full">
          <div className="container mx-auto p-8">
            {selected === 'accountTier' && (
              <div>
                <p className="mb-1 text-2xl text-gray-700">Account Tier</p>
                <hr />
                <br />
                <p className="flex text-lg">
                  Current Tier:
                  <strong className="ml-1">{accountTier}</strong>
                </p>
                <br />
                {privateAccess ? (
                  <p>
                    You have given GitHub Trends (read and write) access to all
                    public and private code contributions. We use your GitHub
                    API access token to make requests on your behalf. All of our
                    code is open-source and visible on our
                    <a
                      className="ml-1 text-blue-500 underline"
                      href="https://github.com/avgupta456/github-trends"
                      rel="noopener noreferrer"
                      target="_blank"
                    >
                      GitHub repository
                    </a>
                  </p>
                ) : (
                  <p>
                    You have given GitHub Trends read access to your public
                    repositories. Upgrading to the Private Workflow will allow
                    us to better represent your code contributions. We use your
                    GitHub API access token to make requests on your behalf. All
                    of our code is open-source and visible on our
                    <a
                      className="ml-1 text-blue-500 underline"
                      href="https://github.com/avgupta456/github-trends"
                      rel="noopener noreferrer"
                      target="_blank"
                    >
                      GitHub repository
                    </a>
                  </p>
                )}
                <br />
                {privateAccess ? (
                  <Button className="bg-gray-200 rounded-sm opacity-50 cursor-not-allowed">
                    Downgrade to Public Access
                  </Button>
                ) : (
                  <a href={GITHUB_PRIVATE_AUTH_URL}>
                    <Button className="bg-blue-500 text-white rounded-sm">
                      Upgrade to Private Access
                    </Button>
                  </a>
                )}
              </div>
            )}
            {selected === 'personalization' && (
              <div>
                <p className="mb-1 text-2xl text-gray-700">Personalization</p>
                <hr />
                <br />
                <p>Coming soon!</p>
              </div>
            )}
            {selected === 'deleteAccount' && (
              <div>
                <p className="mb-1 text-2xl text-gray-700">Delete Account</p>
                <hr />
                <br />
                <p>
                  Deleting your account is permanent and cannot be undone. If
                  you are sure you want to delete your account, click the button
                  below to remove your statistics from GitHub Trends. This will
                  redirect you to a GitHub screen where you can revoke your
                  access token.
                </p>
                <br />
                <Button
                  className="bg-gray-200 rounded-sm text-red-600 border-2"
                  onClick={openDeleteModal}
                >
                  Permenantly Delete Account
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
      {deleteModal && (
        <div>
          <div className="fixed left-0 top-0 w-full h-full">
            <div className="w-full h-full flex justify-center items-center">
              <div
                className="w-96 p-4 bg-white rounded-sm border-2 border-gray-200"
                ref={wrapperRef}
              >
                <p className="mb-1 text-2xl text-gray-700">Delete Account</p>
                <hr />
                <br />
                <p>
                  Are you sure you want to continue? This action cannot be
                  undone.
                </p>
                <br />
                <div className="flex flex-wrap">
                  <Button
                    className="bg-blue-500 text-white rounded-sm"
                    onClick={() => setDeleteModal(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    className="bg-gray-200 ml-auto rounded-sm text-red-600 border-2"
                    onClick={async () => {
                      const success = await deleteAccount(userId, userKey);
                      if (success) {
                        logout();
                        window.location = `https://github.com/settings/connections/applications/${CLIENT_ID}`;
                      }
                    }}
                  >
                    Delete Account
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SettingsScreen;
