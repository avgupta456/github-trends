import math
from typing import List

from external.github_api.graphql.user import (
    get_user_commit_contributions_by_repository as run_query,
)
from models.misc.date import Date, today
from models.user.commit_contributions_by_repository import (
    CommitContribution,
    CommitContributionsByRepository,
    CommitContributions,
    create_commit_contribution,
)


def get_user_commit_contributions_by_repository(
    user_id: str,
    max_repos: int = 100,
    start_date: Date = today - 365,
    end_date: Date = today,
) -> CommitContributions:
    """Gets the daily contribution history for a users top x repositories"""
    time_range = today - start_date  # gets number of days to end date
    segments = min(math.ceil(time_range / 100), 10)  # no more than three years
    raw_repos: List[CommitContributionsByRepository] = []
    commit_contribs_count, repos_with_commit_contrib = 0, 0
    index, cont, after = 0, True, ""  # initialize variables
    while cont and index < segments:
        try:
            data = run_query(user_id, max_repos, after=after)
        except Exception as e:
            raise e

        commit_contribs_count = data.commit_contribs_count
        repos_with_commit_contrib = data.repos_with_commit_contrib

        cont = False
        for i, repo in enumerate(data.commits_by_repo):
            if index == 0:
                raw_repos.append(
                    CommitContributionsByRepository(
                        name=repo.repository.name,
                        contributions=repo.total_count.total_count,
                        contributions_in_range=0,
                        timeline=[],
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
            raw_repos[i].timeline.extend(contribs)

            if repo.contributions.page_info.has_next_page:
                after = repo.contributions.page_info.end_cursor
                cont = True

        index += 1

    # adds contributionsInRange
    for repo in raw_repos:
        repo.contributions_in_range = sum([x.commit_count for x in repo.timeline])

    # converts to objects
    repo_objects = map(
        lambda x: CommitContributionsByRepository.parse_obj(x), raw_repos
    )

    # filters out empty results
    repo_objects = list(filter(lambda x: x.contributions_in_range > 0, repo_objects))

    timeline: List[int] = [0 for _ in range(end_date - start_date + 1)]
    for repo in repo_objects:
        for day in repo.timeline:
            timeline[day.occurred_at - start_date] += day.commit_count

    timeline_object = [
        CommitContribution(occurred_at=start_date + i, commit_count=x)
        for i, x in enumerate(timeline)
    ]

    total_object = CommitContributionsByRepository(
        name="total",
        contributions=commit_contribs_count,
        contributions_in_range=sum(timeline),
        timeline=timeline_object,
    )

    output = CommitContributions(
        commit_contribs_by_repo=list(repo_objects),
        commit_contribs=total_object,
        repos_with_commit_contrib=repos_with_commit_contrib,
    )

    return output
