import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

os.environ["PUBSUB_PUB"] = "True"

# flake8: noqa E402

# add endpoints here (after load dotenv)
from src.routers.users import router as user_router
from src.routers.pubsub import router as pubsub_router
from src.routers.auth import router as auth_router

from src.constants import PROD, PUBSUB_PUB

"""
SETUP
"""

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://githubtrends.io",
    "https://www.githubtrends.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/info")
def get_info():
    return {"PUBSUB_PUB": PUBSUB_PUB, "PROD": PROD}


app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(pubsub_router, prefix="/pubsub", tags=["PubSub"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
