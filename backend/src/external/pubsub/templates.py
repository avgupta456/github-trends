import json
import base64

from typing import Dict, Any

from fastapi import Request, HTTPException

from google.cloud import pubsub_v1  # type: ignore

from src.constants import PROJECT_ID, PUBSUB_TOKEN

publisher = pubsub_v1.PublisherClient()


def publish_to_topic(topic: str, message: Dict[str, Any]) -> None:
    topic_path = publisher.topic_path(PROJECT_ID, topic)  # type: ignore
    data = json.dumps(message).encode("utf-8")
    publisher.publish(topic_path, data=data)  # type: ignore


async def parse_request(token: str, request: Request) -> Dict[str, Any]:
    if token != PUBSUB_TOKEN:
        raise HTTPException(400, "Invalid token")

    data = await request.json()
    data = json.loads(base64.b64decode(data["message"]["data"]))

    return data
