import * as types from '../actions/userActions';

const initialState = {
  userId: JSON.parse(localStorage.getItem('userId')) || null,
  privateAccess: null,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.LOGIN:
      localStorage.setItem('userId', JSON.stringify(action.payload.userId));
      return {
        ...state,
        userId: action.payload.userId,
      };
    case types.LOGOUT:
      localStorage.clear();
      return {
        ...state,
        userId: null,
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
