import requests

s = requests.session()

BASE_URL = "https://api.github.com/"


def get_user(user_id: str) -> dict:
    """
    Returns raw user data
    """
    r = s.get(BASE_URL + "users/" + user_id)
    data = r.json()
    return data


def get_user_followers(user_id: str) -> dict:
    """
    Returns list of followers
    """
    r = s.get(BASE_URL + "users/" + user_id + "/followers")
    data = r.json()
    return data


def get_user_following(user_id: str) -> dict:
    """
    Returns list of following
    """
    r = s.get(BASE_URL + "users/" + user_id + "/following")
    data = r.json()
    return data


def get_user_starred_repos(user_id: str) -> dict:
    """
    Returns list of starred repos
    """
    r = s.get(BASE_URL + "users/" + user_id + "/starred")
    data = r.json()
    return data


def get_user_orgs(user_id: str) -> dict:
    """
    Returns list of user organizations
    """
    r = s.get(BASE_URL + "users/" + user_id + "/orgs")
    data = r.json()
    return data


def get_user_repos(user_id: str) -> dict:
    """
    Returns list of user repositories
    """
    r = s.get(BASE_URL + "users/" + user_id + "/repos")
    data = r.json()
    return data
