import { applyMiddleware, createStore, compose } from 'redux';
import loggerMiddleware from './logger';
import rootReducer from './reducers';

export default function configureStore(intialState) {
  const middlewares = [loggerMiddleware];
  const middlewareEnhancer = applyMiddleware(...middlewares);

  const enhancers = [middlewareEnhancer];
  const composedEnhancers = compose(...enhancers);

  const store = createStore(rootReducer, intialState, composedEnhancers);

  return store;
}
