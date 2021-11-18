import os

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.exceptions import AlreadyExists
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

load_dotenv()

os.environ["PUBSUB_PUB"] = "True"

# flake8: noqa E402

# add endpoints here (after load dotenv)
from src.constants import (
    DOCKER,
    LOCAL_SUBSCRIBER,
    PROD,
    PROJECT_ID,
    PUBSUB_PUB,
    PUBSUB_TOKEN,
    SENTRY_DSN,
)
from src.publisher.routers import (
    asset_router,
    auth_router,
    pubsub_router,
    user_router,
    wrapped_router,
)
from src.utils.pubsub import create_push_subscription, create_topic

"""
EMULATOR SETUP
"""


if not PROD and DOCKER:
    topics = ["user", "wrapped"]
    subscriptions = ["user_sub", "wrapped_sub"]
    endpoints = [
        LOCAL_SUBSCRIBER + "/pubsub/sub/user/" + PUBSUB_TOKEN,
        LOCAL_SUBSCRIBER + "/pubsub/sub/wrapped/" + PUBSUB_TOKEN,
    ]

    for topic, subscription, endpoint in zip(topics, subscriptions, endpoints):
        try:
            print("Creating Topic", PROJECT_ID, topic)
            create_topic(PROJECT_ID, topic)
        except AlreadyExists:
            print("Topic Already Exists")

        try:
            print("Creating Subscription", PROJECT_ID, topic, subscription, endpoint)
            create_push_subscription(PROJECT_ID, topic, subscription, endpoint)
        except AlreadyExists:
            print("Subscription already exists")

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

sentry_sdk.init(
    SENTRY_DSN,
    traces_sample_rate=(1.0 if PROD else 1.0),
)

app.add_middleware(
    SentryAsgiMiddleware,
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/info")
def get_info():
    return {"PUBSUB_PUB": PUBSUB_PUB, "PROD": PROD}


app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(wrapped_router, prefix="/wrapped", tags=["Wrapped"])
app.include_router(pubsub_router, prefix="/pubsub", tags=["PubSub"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(asset_router, prefix="/assets", tags=["Assets"])
