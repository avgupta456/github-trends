from src.models import FullUserPackage, NumericData, ContribStats


def get_contrib_stats(data: FullUserPackage) -> ContribStats:
    return ContribStats.parse_obj(
        {
            "contribs": data.contribs.total_stats.contribs_count,
            "public_contribs": data.contribs.public_stats.contribs_count
            - data.contribs.public_stats.other_count,
            "commits": data.contribs.total_stats.commits_count,
            "public_commits": data.contribs.public_stats.commits_count,
            "issues": data.contribs.total_stats.issues_count,
            "public_issues": data.contribs.public_stats.issues_count,
            "prs": data.contribs.total_stats.prs_count,
            "public_prs": data.contribs.public_stats.prs_count,
            "reviews": data.contribs.total_stats.reviews_count,
            "public_reviews": data.contribs.public_stats.reviews_count,
        }
    )


def get_numeric_data(data: FullUserPackage) -> NumericData:
    return NumericData.parse_obj({"contribs": get_contrib_stats(data)})
