import math
from typing import List

from models.misc.date import Date, today
from models.user.commit_contributions_by_repository import (
    create_commit_contribution,
    CommitContributionsByRepository,
)
from external.github_api.graphql.user import (
    get_user_commit_contributions_by_repository as run_query,
)


def get_user_commit_contributions_by_repository(
    user_id: str,
    max_repos: int = 100,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> List[CommitContributionsByRepository]:
    """Gets the daily contribution history for a users top x repositories"""
    time_range = today - start_date  # gets number of days to end date
    segments = min(math.ceil(time_range / 100), 10)  # no more than three years
    raw_output: List[CommitContributionsByRepository] = []
    index, cont, after = 0, True, ""  # initialize variables
    while cont and index < segments:
        try:
            data = run_query(user_id, max_repos, after=after)
        except Exception as e:
            raise e

        cont = False
        for i, repo in enumerate(data.data):
            if index == 0:
                raw_output.append(
                    CommitContributionsByRepository.parse_obj(
                        {
                            "name": repo.repository.name,
                            "contributions": repo.total_count.total_count,
                            "contributions_in_range": 0,
                            "timeline": [],
                        }
                    )
                )

            raw_contribs = repo.contributions.nodes
            contribs = map(
                lambda x: create_commit_contribution(x),
                raw_contribs,
            )
            contribs = filter(
                lambda x: start_date <= x.occurred_at <= end_date, contribs
            )
            raw_output[i].timeline.extend(contribs)

            if repo.contributions.page_info.has_next_page:
                after = repo.contributions.page_info.end_cursor
                cont = True

        index += 1

    # adds contributionsInRange
    for repo in raw_output:
        repo.contributions_in_range = sum([x.commit_count for x in repo.timeline])

    # converts to objects
    output_objects = map(
        lambda x: CommitContributionsByRepository.parse_obj(x), raw_output
    )

    # filters out empty results
    output_objects = filter(lambda x: x.contributions_in_range > 0, output_objects)

    return list(output_objects)
