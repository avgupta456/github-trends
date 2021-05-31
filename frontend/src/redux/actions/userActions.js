export const LOGIN = 'LOGIN';
export const LOGOUT = 'LOGOUT';

export function login(userId) {
  return { type: LOGIN, payload: { userId } };
}

export function logout() {
  return { type: LOGOUT, payload: {} };
}
