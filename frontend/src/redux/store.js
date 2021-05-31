import { applyMiddleware, createStore, compose } from 'redux';

import loggerMiddleware from './logger';
import rootReducer from './reducers';
import { USE_LOGGER } from '../constants';

export default function configureStore(intialState) {
  let middlewares = [];
  if (USE_LOGGER) {
    middlewares = [loggerMiddleware];
  }
  const middlewareEnhancer = applyMiddleware(...middlewares);

  const enhancers = [middlewareEnhancer];
  const composedEnhancers = compose(...enhancers);

  const store = createStore(rootReducer, intialState, composedEnhancers);

  return store;
}
