# type: ignore

from typing import Any, Dict, List

# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
datastore_client = datastore.Client()


def set_access_token(user_id: str, access_token: str) -> None:
    obj_key = datastore_client.key("ID_AT", user_id)
    obj = datastore.Entity(key=obj_key)
    obj["user_id"] = user_id
    obj["access_token"] = access_token
    datastore_client.put(obj)


def get_access_token(user_id: str) -> str:
    obj_key = datastore_client.key("ID_AT", user_id)
    obj = datastore_client.get(obj_key)
    if obj is not None and "access_token" in obj:
        return obj["access_token"]
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


def get_all_user_ids() -> List[str]:
    data: List[Any] = list(datastore_client.query(kind="ID_AT").fetch())
    data = [x["user_id"] for x in data]
    print(data)
    return data
