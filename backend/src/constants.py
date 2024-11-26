import os

# GLOBAL
LOCAL = os.getenv("LOCAL", "False") == "True"
PROD = os.getenv("PROD", "False") == "True"
PROJECT_ID = "github-334619"
BACKEND_URL = "https://api.githubtrends.io" if PROD else "http://localhost:8000"

OWNER = "avgupta456"
REPO = "github-trends"

# API
# https://docs.github.com/en/rest/reference/rate-limit
# https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits
# https://docs.github.com/en/graphql/overview/resource-limitations
TIMEOUT = 15  # max seconds to wait for api response
GRAPHQL_NODE_CHUNK_SIZE = 50  # number of nodes (commits) to query (max 100)
GRAPHQL_NODE_THREADS = 5  # number of node queries simultaneously (avoid blacklisting)
REST_NODE_THREADS = 50  # number of node queries simultaneously (avoid blacklisting)

PR_FILES = 5  # max number of files to query for PRs
NODE_QUERIES = 20  # max number of node queries to make
CUTOFF = 1000  # if additions or deletions > CUTOFF, or sum > 2 * CUTOFF, ignore LOC
FILE_CUTOFF = 1000  # if less than cutoff in file, count LOC

API_VERSION = 0.02  # determines when to overwrite MongoDB data

# CUSTOMIZATION
BLACKLIST = ["Jupyter Notebook", "HTML"]  # languages to ignore

# OAUTH
prefix = "PROD" if PROD else "DEV"
# client ID for GitHub OAuth App
OAUTH_CLIENT_ID = os.getenv(f"{prefix}_OAUTH_CLIENT_ID", "")
# client secret for App
OAUTH_CLIENT_SECRET = os.getenv(f"{prefix}_OAUTH_CLIENT_SECRET", "")
# redirect uri for App
OAUTH_REDIRECT_URI = os.getenv(f"{prefix}_OAUTH_REDIRECT_URI", "")

# MONGODB
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")

# SVG
DEFAULT_COLOR = "#858585"

# SENTRY
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# TESTING
TEST_USER_ID = "avgupta456"
TEST_REPO = "github-trends"
TEST_TOKEN = os.getenv("AUTH_TOKEN", "")  # for authentication
TEST_NODE_IDS = [
    "C_kwDOENp939oAKGM1MzdlM2QzMTZjMmEyZGIyYWU4ZWI0MmNmNjQ4YWEwNWQ5OTBiMjM",
    "C_kwDOD_-BVNoAKDFhNTIxNWE1MGM4ZDllOGEwYTFhNjhmYWZkYzE5MzA5YTRkMDMwZmM",
    "C_kwDOD_-BVNoAKDRiZTQ4MTQ0MzgwYjBlNGEwNjQ4YjY4YWI4ZjFjYmQ3MWU4M2VhMzU",
]
TEST_SHA = "ad83e6340377904fa0295745b5314202b23d2f3f"

# WRAPPED

# example users, don't need to star the repo
USER_WHITELIST = [
    "torvalds",
    "yyx990803",
    "shadcn",
    "sindresorhus",
]

USER_BLACKLIST = ["kangmingtay", "ae7er", "stalukdar7", "piyush7833"]

print("PROD", PROD)
print("API_VERSION", API_VERSION)
print()
