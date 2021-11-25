# FAQ

The FAQ is in progress. Reach out if you have any unanswered questions or concerns.

---

**Question**: Does GitHub Trends have access to my private code contributions?

**Answer**: GitHub Trends requires an OAuth access token to make requests on your behalf. The standard public workflow creates a token with read-only access to strictly public information. **This access token can not view or edit any private contributions**.

Alternatively, users can use the private workflow which creates a token with read and write access to private information. Although GitHub Trends only uses it's read access, GitHub does not allow read-only private access (see [an open issue from 2015](https://github.com/jollygoodcode/jollygoodcode.github.io/issues/6)). While one may scan the repository to confirm this statement, there are inherent security risks to this overallocation. If this poses an issue to you, please use the public workflow instead.

**Question**: How can I display my images side by side?

**Answer**: Use HTML (credit: [github-readme-stats](https://github.com/anuraghazra/github-readme-stats#quick-tip-align-the-repo-cards))

```
<a href="https://githubtrends.io">
  <img align="center" src="https://api.githubtrends.io/user/svg/avgupta456/langs" />
</a>
<a href="https://githubtrends.io">
  <img align="center" src="https://api.githubtrends.io/user/svg/avgupta456/repos" />
</a>
```

**Question**: What if I find a bug, or want to contribute?

**Answer**: Raise an [issue](https://github.com/avgupta456/github-trends/issues/new) or [pull request](https://github.com/avgupta456/github-trends/compare) through GitHub. I would be happy to discuss and implement any suggestions or improvements.
