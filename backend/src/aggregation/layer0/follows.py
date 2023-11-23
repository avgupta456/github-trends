from typing import List, Optional

from src.data.github.graphql import (
    get_user_followers as _get_user_followers,
    get_user_following as _get_user_following,
)
from src.models import User, UserFollows


def get_user_follows(user_id: str, access_token: Optional[str]) -> UserFollows:
    """get user followers and users following for given user"""

    followers: List[User] = []
    following: List[User] = []

    for user_list, get_func in zip(
        [followers, following], [_get_user_followers, _get_user_following]
    ):
        after: Optional[str] = ""
        index, cont = 0, True  # initialize variables
        while cont and index < 10:
            after_str: str = after if isinstance(after, str) else ""
            data = get_func(user_id, after=after_str, access_token=access_token)

            cont = False

            user_list.extend(
                map(
                    lambda x: User(name=x.name, login=x.login, url=x.url),
                    data.nodes,
                )
            )
            if data.page_info.has_next_page:
                after = data.page_info.end_cursor
                cont = True

            index += 1

    return UserFollows(followers=followers, following=following)
