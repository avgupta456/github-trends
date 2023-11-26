import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';

import configureStore from './redux/store';
import { AppTrends, AppWrapped } from './pages/App';
import './index.css';

import { MODE } from './constants';

export const store = configureStore();

const root = ReactDOM.createRoot(document.getElementById('root'));

if (MODE === 'trends') {
  root.render(
    <Provider store={store}>
      <AppTrends />
    </Provider>,
  );
} else if (MODE === 'wrapped') {
  root.render(
    <Provider store={store}>
      <AppWrapped />
    </Provider>,
  );
} else {
  // Throw an error if the mode is not set correctly.
  throw new Error(
    'REACT_APP_MODE must be set to "trends" or "wrapped" in your .env file.',
  );
}
