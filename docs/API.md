# GitHub Trends API

GitHub Trends provides two methods to access GitHub Trends data: the Website Workflow at githubtrends.io and the API Workflow described below.

## Available Cards

After authenticating with either the public or private workflow (see below), users can create the following cards to display their GitHub Trends data:

- **[Languages Card](https://github.com/avgupta456/github-trends/blob/main/docs/API.md#languages-card)**: See your top languages over a given time interval, based on all commits to personal and open-source repositories.

- **[Repositories Card](https://github.com/avgupta456/github-trends/blob/main/docs/API.md#repositories-card)**: See your top repositories based on lines of code contributed over a given time period. This includes both personal and open-source repositories.

# Authentication

You will need to create an account with GitHub Trends to create cards. The account is used to assosciate queries to the GitHub API made on your behalf with your GitHub account's API quota. We use less than 5% of your quota in almost all scenarios. There are two levels of authentication possible:

- Public Workflow: The Public Workflow asks for read-only permission to public information. This will allow us to analyze your public contributions and repositories only.
- Private Workflow: The Private Workflow asks for read and write permission to public and private information. This will allow us to analyze your entire contribution history. See [the FAQ](https://github.com/avgupta456/github-trends/blob/main/docs/FAQ.md) for further information.

You will only need to authenticate once with GitHub Trends. Subsequent requests will use your stored access token.

For the public workflow, visit

```md
https://api.githubtrends.io/auth/signup/public
```

For the private workflow, visit

```md
https://api.githubtrends.io/auth/signup/private
```

You will be prompted to allow access, and (hopefully) redirected to a success screen.

If you have previously authenticated with the public workflow, you can upgrade to the private workflow by using the private link. If you would like to delete your account, go to your GitHub settings and revoke the access token.

# Languages Card

See your top languages over a given time interval, based on all commits to personal and open-source repositories. Your top five languages will be displayed. Due to the approximations used internally, LOC metrics will be rounded to the nearest 100 lines.

After authentication, visit

```md
https://api.githubtrends.io/user/svg/{user_id}/langs
```

## Customization

The following customization options are available:

| Option            | Description                                                                                                                                | Default     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| `time_range`      | Specifies the time range to query statistics for. Valid options are `one_month`, `three_months`, `six_months`, `one_year`, and `all_time`. | `one_month` |
| `include_private` | Determines if private contributions are included (requires private workflow).                                                              | `false`     |
| `compact`         | Determines if compact layout is used (forces percentages over LOC)                                                                         | `false`     |
| `use_percent`     | Valid if `compact=false`, determines if line of code (default) or percentages are displayed.                                               | `false`     |
| `loc_metric`      | Options are LOC added (`added`) and LOC changed (`changed`).                                                                               | `added`     |
| `theme`           | Theme to use for the card. See [docs/THEME.md](https://github.com/avgupta456/github-trends/blob/main/docs/THEME.md) for options.           | `classic`   |

Customizations can be appended to the endpoint, separated first with `?` and subsequently with `&`.

## Example

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=three_months&include_private=true&compact=true`

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=three_months&include_private=true&compact=true)](https://githubtrends.io)

# Repositories Card

After authentication, visit

```md
https://api.githubtrends.io/user/svg/{user_id}/repos
```

## Customization

The following customization options are available:

| Option            | Description                                                                                                                                | Default     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| `time_range`      | Specifies the time range to query statistics for. Valid options are `one_month`, `three_months`, `six_months`, `one_year`, and `all_time`. | `one_month` |
| `include_private` | Determines if private contributions are included (requires private workflow).                                                              | `false`     |
| `group`           | Options are `none` (default), `other` (group all other repos together), and `private` (force private repos to be grouped)                  | `none`      |
| `use_percent`     | Valid if `compact=false`, determines if line of code (default) or percentages are displayed.                                               | `false`     |
| `loc_metric`      | Options are LOC added (`added`) and LOC changed (`changed`).                                                                               | `added`     |
| `theme`           | Theme to use for the card. See [docs/THEME.md](https://github.com/avgupta456/github-trends/blob/main/docs/THEME.md) for options.           | `classic`   |

Customizations can be appended to the endpoint, separated first with `?` and subsequently with `&`.

## Example

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=true&group=private&loc_metric=changed&theme=dark`

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=true&group=private&loc_metric=changed&theme=dark)](https://githubtrends.io)
