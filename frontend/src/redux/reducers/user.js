import * as types from '../actions/userActions';

const initialState = {
  isLoggedIn: JSON.parse(localStorage.getItem('isLoggedIn')) || false,
  userId: JSON.parse(localStorage.getItem('userId')) || null,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.LOGIN:
      localStorage.setItem('isLoggedIn', JSON.stringify(true));
      localStorage.setItem('userId', JSON.stringify(action.payload.userId));
      return {
        ...state,
        isLoggedIn: true,
        userId: action.payload.userId,
      };
    case types.LOGOUT:
      localStorage.clear();
      return {
        ...state,
        isLoggedIn: false,
        userId: null,
      };
    default:
      return state;
  }
};
