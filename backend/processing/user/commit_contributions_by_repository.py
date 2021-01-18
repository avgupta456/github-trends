import logging
from typing import Optional, List, Dict, Any

from models.misc.date import Date, today
from models.user.commit_contributions_by_repository import (
    CommitContribution,
    CommitContributionsByRepository,
)
from external.github_api.graphql.user import (
    get_user_commit_contributions_by_repository as run_query,
)


def get_user_commit_contributions_by_repository(
    user_id: str,
    max_repos: Optional[int] = 10,
    start_date: Optional[Date] = today - 365,
    end_date: Optional[Date] = today,
) -> List[CommitContributionsByRepository]:
    """Gets the daily contribution history for a users top x repositories"""
    output = []
    index, cont, after = 0, True, ""
    while index < 10 and cont:
        try:
            data = run_query(user_id, max_repos, after=after)
        except Exception as e:
            logging.exception(e)
            raise e

        data = data["data"]["user"]["contributionsCollection"][
            "commitContributionsByRepository"
        ]

        cont = False
        repo: Dict[str, Any]
        for i, repo in enumerate(data):
            if index == 0:
                output.append(
                    {
                        "name": repo["repository"]["name"],
                        "contributions": repo["totalCount"]["totalCount"],
                        "timeline": [],
                    }
                )

            raw_contribs = repo["contributions"]["nodes"]
            print(raw_contribs[0])
            print(CommitContribution.parse_obj(raw_contribs[0]))
            contribs = map(lambda x: CommitContribution.parse_obj(x), raw_contribs)
            output[i]["timeline"].extend(contribs)

            if repo["contributions"]["pageInfo"]["hasNextPage"]:
                after = repo["contributions"]["pageInfo"]["endCursor"]
                cont = True

        index += 1

    output = list(map(lambda x: CommitContributionsByRepository.parse_obj(x), output))
    return output
