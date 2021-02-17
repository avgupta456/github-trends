import * as types from '../actions/userActions';

const initialState = {
  userId: '',
  userData: {},
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.SET_USER_ID:
      return {
        ...state,
        userId: action.payload.userId,
      };
    case types.SET_USER_DATA:
      return {
        ...state,
        userData: action.payload.userData,
      };
    default:
      return state;
  }
};
