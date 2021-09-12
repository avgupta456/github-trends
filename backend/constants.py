import os

USER_ID = "AshishGupta938"  # for testing, previously "avgupta456"
TOKEN = os.getenv("AUTH_TOKEN", "")  # for authentication
TIMEOUT = 3  # max seconds to wait for api response

NODE_CHUNK_SIZE = 50  # number of nodes (commits) to query (max 100)
NODE_THREADS = 30  # number of node queries simultaneously (avoid blacklisting)

BLACKLIST = ["Jupyter Notebook", "HTML"]  # languages to ignore
CUTOFF = 1000  # if > cutoff lines, assume imported, don't count

OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "")  # client ID for GitHub OAuth App
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "")  # client secret for App
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "")  # redirect uri for App

PROD = os.getenv("PROD", "False") == "True"
PUBSUB_PUB = os.getenv("PUBSUB_PUB", "False") == "True"
