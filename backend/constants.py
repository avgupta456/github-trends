import os


TOKEN = os.getenv("AUTH_TOKEN", "")  # for authentication
TIMEOUT = 3  # max seconds to wait for api response

NODE_CHUNK_SIZE = 50  # number of nodes (commits) to query (max 100)
NODE_THREADS = 30  # number of node queries simultaneously (avoid blacklisting)

BLACKLIST = ["Jupyter Notebook"]  # languages to ignore
CUTOFF = 1000  # if > cutoff lines, assume imported, don't count
