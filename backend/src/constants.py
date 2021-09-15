import os

# GLOBAL
PROD = os.getenv("PROD", "False") == "True"
PROJECT_ID = "github-298920"

# API
TIMEOUT = 3  # max seconds to wait for api response
NODE_CHUNK_SIZE = 50  # number of nodes (commits) to query (max 100)
NODE_THREADS = 30  # number of node queries simultaneously (avoid blacklisting)
CUTOFF = 1000  # if > cutoff lines, assume imported, don't count

# CUSTOMIZATION
BLACKLIST = ["Jupyter Notebook", "HTML"]  # languages to ignore

# OAUTH
OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "")  # client ID for GitHub OAuth App
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "")  # client secret for App
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "")  # redirect uri for App

# PUBSUB
PUBSUB_PUB = os.getenv("PUBSUB_PUB", "False") == "True"
PUBSUB_TOKEN = os.getenv("PUBSUB_TOKEN", "")
LOCAL_SUBSCRIBER = "localhost:8001/pubsub/"

# MONGODB
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")

# TESTING
TEST_USER_ID = "AshishGupta938"  # for testing, previously "avgupta456"
TEST_TOKEN = os.getenv("AUTH_TOKEN", "")  # for authentication
