export const SET_USER_ID = 'SET_USER_ID';
export const SET_USER_DATA = 'SET_USER_DATA';

export function setUserId(userId) {
  return { type: SET_USER_ID, payload: { userId } };
}

export function setUserData(userData) {
  return { type: SET_USER_DATA, payload: { userData } };
}
