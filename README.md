# GitHub Trends

[![Coverage Status](https://coveralls.io/repos/github/avgupta456/github-trends/badge.svg?t=jQQ3FK)](https://coveralls.io/github/avgupta456/github-trends)

## What is GitHub Trends

GitHub Trends dives deep into the GitHub API to bring you exciting and impactful metrics about your code contributions. Generate insights on lines written by language, commit frequency by date and time, repository contribution rankings, and more. Check out some of the examples below:

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=True)](https://githubtrends.io)

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=one_year&include_private=True&compact=True)](https://githubtrends.io)

## How to use

Visit [githubtrends.io](https://www.githubtrends.io) to create an account and get started!

## FAQ

**Question**: Does GitHub Trends have access to my private code contributions?

**Answer**: GitHub Trends requires an OAuth access token to make requests on your behalf. The standard public workflow creates a token with read-only access to strictly public information. **This access token can not view or edit any private contributions**.

Alternatively, users can use the private workflow which creates a token with read and write access to private information. Although GitHub Trends only uses it's read access, GitHub does not allow read-only private access (see [an open issue from 2015](https://github.com/jollygoodcode/jollygoodcode.github.io/issues/6)). While one may scan the repository to confirm this statement, there are inherent security risks to this overallocation. If this poses an issue to you, please use the public workflow instead.

## Contributing

See `CONTRIBUTING.md`.
