import * as types from '../actions/userActions';

const initialState = {
  userId: JSON.parse(localStorage.getItem('userId')) || null,
  userKey: JSON.parse(localStorage.getItem('userKey')) || null,
  privateAccess: null,
};

// eslint-disable-next-line default-param-last
export default (state = initialState, action) => {
  switch (action.type) {
    case types.LOGIN:
      localStorage.setItem('userId', JSON.stringify(action.payload.userId));
      localStorage.setItem('userKey', JSON.stringify(action.payload.userKey));
      return {
        ...state,
        userId: action.payload.userId,
        userKey: action.payload.userKey,
      };
    case types.LOGOUT:
      localStorage.clear();
      return {
        userId: null,
        userKey: null,
        privateAccess: null,
      };
    case types.SET_PRIVATE_ACCESS:
      return {
        ...state,
        privateAccess: action.payload.privateAccess,
      };
    default:
      return state;
  }
};
