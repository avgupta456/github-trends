# GitHub Trends

[![Coverage Status](https://coveralls.io/repos/github/avgupta456/github-trends/badge.svg?t=jQQ3FK)](https://coveralls.io/github/avgupta456/github-trends)

## What is GitHub Trends

GitHub Trends dives deep into the GitHub API to bring you exciting and impactful metrics about your code contributions. Generate insights on lines written by language, commit frequency by date and time, repository contribution rankings, and more. Check out some of the examples below:

<a href="https://githubtrends.io">
  <img align="center" src="https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=one_year&include_private=True" />
</a>
<a href="https://githubtrends.io">
  <img align="center" src="https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=True" />
</a>

---

# Usage

## Website Workflow (Alpha)

Visit [githubtrends.io](https://www.githubtrends.io) to create an account and get started!

Have questions? Check out [the demo](https://www.githubtrends.io/demo)!

![image](https://user-images.githubusercontent.com/16708871/138611082-105e4dbc-8a27-4f68-8045-f9d86c912429.png)

---

## API Workflow (Alpha)

Alternatively, you can communicate directly with the API to create and customize your cards.

### Authentication

You will need to create an account with GitHub Trends to create cards. The account is used to assosciate queries to the GitHub API made on your behalf with your GitHub account's API quota. We use less than 5% of your quota in almost all scenarios. There are two levels of authentication possible:

- Public Workflow: The Public Workflow asks for read-only permission to public information. This will allow us to analyze your public contributions and repositories only.
- Private Workflow: The Private Workflow asks for read and write permission to public and private information. This will allow us to analyze your entire contribution history. See [the FAQ](https://github.com/avgupta456/github-trends#FAQ) for further information.

You will only need to authenticate once with GitHub Trends. Subsequent requests will use your stored access token.

For the public workflow, visit

```
https://api.githubtrends.io/auth/signup/public
```

For the private workflow, visit

```
https://api.githubtrends.io/auth/signup/private
```

You will be prompted to allow access, and (hopefully) redirected to a success screen.

If you have previously authenticated with the public workflow, you can upgrade to the private workflow by using the private link. If you would like to delete your account, go to your GitHub settings and revoke the access token.

---

## Available Cards

- **Languages Card**: See your top languages over a given time interval, based on all commits to personal and open-source repositories. Visit [the documentation](https://github.com/avgupta456/github-trends#languages-card).

- **Repositories Card**: See your top repositories based on LOC contributed over a given time period. This includes both personal and open-source repositories. Visit [the documentation](https://github.com/avgupta456/github-trends#repositories-card).

---

## Languages Card

See your top languages over a given time interval, based on all commits to personal and open-source repositories. Your top five languages will be displayed. Due to the approximations used internally, LOC metrics will be rounded to the nearest 100 lines.

After authentication, visit

```
https://api.githubtrends.io/user/svg/{user_id}/langs
```

### Customization

The following customization options are available:

- `time_range`: valid options are `one_month`, `three_months`, `six_months`, and `one_year`. Specifies the time range to query. Default value is `one_month`
- `start_date`, `end_date`: if `time_range` is not supplied or invalid, `start_date` and `end_date` define the bounds of the time range (format: YYYY-MM-DD). Default `start_date` is `today() - 30`, default `end_date` is `today()`
- `include_private`: determines if private contributions are included (requires private workflow). Default is `false`
- `compact`: determines if compact layout is used (forces percentages over LOC). Default is `false`
- `use_percent`: Valid if `compact=false`, determines if lines of code (default) or percentages are displayed. Default is `false`
- `loc_metric`: Options are LOC added (`added`) and LOC changed (`changed`), default is `added`.

Customizations can be appended to the endpoint, separated first with `?` and subsequently with `&`.

### Examples

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=three_months&include_private=true&compact=true`

Embeddable Link:

```
[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=three_months&include_private=true&compact=true)](https://githubtrends.io)
```

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=three_months&include_private=true&compact=true)](https://githubtrends.io)

---

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=one_year&include_private=true&loc_metric=changed`

Embeddable Link:

```
[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=one_year&include_private=true&loc_metric=changed)](https://githubtrends.io)
```

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/langs?time_range=one_year&include_private=true&loc_metric=changed)](https://githubtrends.io)

---

## Repositories Card

After authentication, visit

```
https://api.githubtrends.io/user/svg/{user_id}/repos
```

### Customization

The following customization options are available:

- `time_range`: valid options are `one_month`, `three_months`, `six_months`, and `one_year`. Specifies the time range to query. Default value is `one_month`
- `start_date`, `end_date`: if `time_range` is not supplied or invalid, `start_date` and `end_date` define the bounds of the time range (format: YYYY-MM-DD). Default `start_date` is `today() - 30`, default `end_date` is `today()`
- `include_private`: determines if private contributions are included (requires private workflow). Default is `false`
- `use_percent`: Valid if `compact=false`, determines if lines of code (default) or percentages are displayed. Default is `false`
- `loc_metric`: Options are LOC added (`added`) and LOC changed (`changed`), default is `added`.

### Examples

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=three_months&include_private=true`

Embeddable Link:

```
[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=three_months&include_private=true)](https://githubtrends.io)
```

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=three_months&include_private=true)](https://githubtrends.io)

---

Endpoint: `https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=true&loc_metric=changed`

Embeddable Link:

```
[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=true&loc_metric=changed)](https://githubtrends.io)
```

[![GitHub Trends SVG](https://api.githubtrends.io/user/svg/avgupta456/repos?time_range=one_year&include_private=true&loc_metric=changed)](https://githubtrends.io)

---

# FAQ

**Question**: Does GitHub Trends have access to my private code contributions?

**Answer**: GitHub Trends requires an OAuth access token to make requests on your behalf. The standard public workflow creates a token with read-only access to strictly public information. **This access token can not view or edit any private contributions**.

Alternatively, users can use the private workflow which creates a token with read and write access to private information. Although GitHub Trends only uses it's read access, GitHub does not allow read-only private access (see [an open issue from 2015](https://github.com/jollygoodcode/jollygoodcode.github.io/issues/6)). While one may scan the repository to confirm this statement, there are inherent security risks to this overallocation. If this poses an issue to you, please use the public workflow instead.

**Question**: How can I display my images side by side?

**Answer**: Use HTML (credit: [github-readme-stats](https://github.com/anuraghazra/github-readme-stats#quick-tip-align-the-repo-cards))

```
<a href="https://github.com/anuraghazra/github-readme-stats">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=anuraghazra&repo=github-readme-stats" />
</a>
<a href="https://github.com/anuraghazra/convoychat">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=anuraghazra&repo=convoychat" />
</a>
```

**Question**: What if I find a bug, or want to contribute?

**Answer**: Raise an [issue](https://github.com/avgupta456/github-trends/issues/new) or [pull request](https://github.com/avgupta456/github-trends/compare) through GitHub. I would be happy to discuss and implement any suggestions or improvements.

## Contributing

See `CONTRIBUTING.md`.

## Acknowledgements

- Much inspiration was taken from https://github.com/anuraghazra/github-readme-stats. If you haven't already, check it out and give it a star!
