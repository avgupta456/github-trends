import * as types from '../actions/userActions';

const initialState = {
  userId: JSON.parse(localStorage.getItem('userId')) || null,
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
    default:
      return state;
  }
};
