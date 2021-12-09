import os

# GLOBAL
PROD = os.getenv("PROD", "False") == "True"
DOCKER = os.getenv("DOCKER", "False") == "True"
PROJECT_ID = "github-334619"
BACKEND_URL = "https://api.githubtrends.io" if PROD else "http://localhost:8000"

# API
# https://docs.github.com/en/rest/reference/rate-limit
# https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits
# https://docs.github.com/en/graphql/overview/resource-limitations
TIMEOUT = 15  # max seconds to wait for api response
NODE_CHUNK_SIZE = 100  # number of nodes (commits) to query (max 100)
NODE_THREADS = 5  # number of node queries simultaneously (avoid blacklisting)

PR_FILES = 5  # max number of files to query for PRs
NODE_QUERIES = 20  # max number of node queries to make
CUTOFF = 2000  # if less than cutoff, count LOC
FILE_CUTOFF = 1000  # if less than cutoff in file, count LOC

WRAPPED_VERSION = 0.04  # determines when to overwrite MongoDB data

# CUSTOMIZATION
BLACKLIST = ["Jupyter Notebook", "HTML"]  # languages to ignore

# OAUTH
OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "")  # client ID for GitHub OAuth App
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "")  # client secret for App
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "")  # redirect uri for App

# PUBSUB
PUBSUB_PUB = os.getenv("PUBSUB_PUB", "False") == "True"
PUBSUB_TOKEN = os.getenv("PUBSUB_TOKEN", "")
LOCAL_SUBSCRIBER = "http://" + ("subscriber" if DOCKER else "localhost") + ":8001"
LOCAL_PUBLISHER = BACKEND_URL if not DOCKER else "http://publisher:8000"


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
