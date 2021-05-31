# type: ignore

from typing import Any, Dict

# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
datastore_client = datastore.Client()


def set_access_token(user_id: str, access_token: str) -> None:
    obj_key_1 = datastore_client.key("ID_AT", user_id)
    obj_1 = datastore.Entity(key=obj_key_1)
    obj_1["access_token"] = access_token
    datastore_client.put(obj_1)
    obj_key_2 = datastore_client.key("AT_ID", access_token)
    obj_2 = datastore.Entity(key=obj_key_2)
    obj_2["user_id"] = user_id
    datastore_client.put(obj_2)


def get_access_token(user_id: str) -> str:
    obj_key = datastore_client.key("ID_AT", user_id)
    obj = datastore_client.get(obj_key)
    if obj is not None and "access_token" in obj:
        return obj["access_token"]
    return ""


def get_user_id(access_token: str) -> str:
    obj_key = datastore_client.key("AT_ID", access_token)
    obj = datastore_client.get(obj_key)
    if obj is not None and "user_id" in obj:
        return obj["user_id"]
    return ""


def set_user_endpoint(user_id: str, data: Dict[str, Any]) -> None:
    obj_key = datastore_client.key("User_Data", user_id)
    obj = datastore.Entity(key=obj_key)
    obj["data"] = data
    datastore_client.put(obj)


def get_user_endpoint(user_id: str) -> Any:
    obj_key = datastore_client.key("User_Data", user_id)
    obj = datastore_client.get(obj_key)
    if obj is not None and "data" in obj:
        return obj["data"]
    return None
