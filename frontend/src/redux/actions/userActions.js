export const LOGIN = 'LOGIN';
export const LOGOUT = 'LOGOUT';
export const SET_PRIVATE_ACCESS = 'SET_PRIVATE_ACCESS';

export function login(userId, userKey) {
  return { type: LOGIN, payload: { userId, userKey } };
}

export function logout() {
  return { type: LOGOUT, payload: {} };
}

export function setPrivateAccess(privateAccess) {
  return { type: SET_PRIVATE_ACCESS, payload: { privateAccess } };
}
