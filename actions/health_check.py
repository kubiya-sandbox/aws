from typing import List

import boto3
from pydantic import BaseModel

from ..main_store import store as s
# from ..aws.actions import action_store as s


class HealthRequest(BaseModel):
    pass


class HealthResponse(BaseModel):
    params: bool
    connection: bool
    errors: List[str]


@s.kubiya_action()
def health_check(_: HealthRequest) -> HealthResponse:
    errors = List[str]
    params = _validate_params(errors)
    connection = _validate_conn(errors)
    return HealthResponse(params=params, connection=connection, errors=errors)


def _validate_conn(e: List[str]) -> bool:
    try:
        c = boto3.client(
            "ecs",
            aws_access_key_id=s.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=s.secrets["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=s.secrets["AWS_SESSION_TOKEN"],
            region_name=s.secrets["AWS_DEFAULT_REGION"],
        )
        return c.list_clusters().get("clusterArns") is not None
    except Exception as e:
        e.append(f"faild to connect to aws: {str(e)}")
        return False


def _validate_params(e: List[str]) -> bool:
    valid = True

    if s.secrets.get("AWS_ACCESS_KEY_ID") == "":
        valid = False
        e.append("AWS_ACCESS_KEY_ID is not set")

    if s.secrets.get("AWS_SESSION_TOKEN") == "":
        valid = False
        e.append("AWS_SESSION_TOKEN is not set")

    if s.secrets.get("AWS_DEFAULT_REGION") == "":
        valid = False
        e.append("AWS_DEFAULT_REGION is not set")

    if s.secrets.get("AWS_SECRET_ACCESS_KEY") == "":
        valid = False
        e.append("AWS_SECRET_ACCESS_KEY is not set")

    return valid
