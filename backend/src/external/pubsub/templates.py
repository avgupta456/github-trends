import json
import base64
import requests

from typing import Dict, Any

from fastapi import Request, HTTPException

from google.cloud import pubsub_v1  # type: ignore

from src.constants import PROD, PROJECT_ID, PUBSUB_PUB, PUBSUB_TOKEN, LOCAL_SUBSCRIBER

publisher = pubsub_v1.PublisherClient()


def publish_to_topic(topic: str, message: Dict[str, Any]) -> None:
    if PROD and not PUBSUB_PUB:
        raise HTTPException(400, "Publishing is disabled")

    data = json.dumps(message).encode("utf-8")
    if PROD:
        topic_path = publisher.topic_path(PROJECT_ID, topic)  # type: ignore
        publisher.publish(topic_path, data=data)  # type: ignore
    else:
        requests.post(LOCAL_SUBSCRIBER + topic + "/" + PUBSUB_TOKEN, data=data)


async def parse_request(token: str, request: Request) -> Dict[str, Any]:
    if PROD and PUBSUB_PUB:
        raise HTTPException(400, "Subscribing is disabled")
    if token != PUBSUB_TOKEN:
        raise HTTPException(400, "Invalid token")

    data = await request.json()
    if PROD:
        data = json.loads(base64.b64decode(data["message"]["data"]))

    return data
