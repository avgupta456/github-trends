import requests

s = requests.session()

BASE_URL = "https://api.github.com/users/"


def get_user(user_id: str) -> dict:
    """
    Returns raw user data
    """
    r = s.get(BASE_URL + user_id)
    return r.json()


def get_user_followers(user_id: str) -> dict:
    """
    Returns list of followers
    """
    r = s.get(BASE_URL + user_id + "/followers")
    return r.json()


def get_user_following(user_id: str) -> dict:
    """Returns list of following"""
    r = s.get(BASE_URL + user_id + "/following")
    return r.json()


def get_user_starred_repos(user_id: str) -> dict:
    """Returns list of starred repos"""
    r = s.get(BASE_URL + user_id + "/starred")
    return r.json()


def get_user_orgs(user_id: str) -> dict:
    """Returns list of user organizations"""
    r = s.get(BASE_URL + user_id + "/orgs")
    return r.json()


def get_user_repos(user_id: str) -> dict:
    """Returns list of user repositories"""
    r = s.get(BASE_URL + user_id + "/repos")
    return r.json()
