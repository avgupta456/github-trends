from typing import Dict

import sentry_sdk
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

load_dotenv(find_dotenv())

# flake8: noqa E402

# add endpoints here (after load dotenv)
from src.constants import PROD, SENTRY_DSN
from src.routers import (
    asset_router,
    auth_router,
    dev_router,
    user_router,
    wrapped_router,
)

"""
SETUP
"""

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://githubtrends.io",
    "https://www.githubtrends.io",
    "https://githubwrapped.io",
    "https://www.githubwrapped.io",
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
async def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/info")
def get_info() -> Dict[str, bool]:
    return {"PROD": PROD}


app.include_router(asset_router, prefix="/assets", tags=["Assets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(dev_router, prefix="/dev", tags=["Dev"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(wrapped_router, prefix="/wrapped", tags=["Wrapped"])
