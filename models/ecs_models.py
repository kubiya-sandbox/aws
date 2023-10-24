from pydantic import BaseModel
from typing import List, Optional


class RegisterTaskDefinitionRequest(BaseModel):
    family: str
    taskRoleArn: str
    executionRoleArn: str
    networkMode: str
    containerDefinitions: List[dict]
    placementConstraints: List[dict] = None
    requiresCompatibilities: List[str] = None
    cpu: str = None
    memory: str = None
    volumes: List[dict] = None
    placementStrategy: List[dict] = None
    tags: List[dict] = None


class RegisterTaskDefinitionResponse(BaseModel):
    task_definition: dict


class DeregisterTaskDefinitionRequest(BaseModel):
    task_definition_arn: str


class DeregisterTaskDefinitionResponse(BaseModel):
    task_definition_arn: str
    error_message: Optional[str]


class DescribeTaskDefinitionRequest(BaseModel):
    task_definition_arn: str


class DescribeTaskDefinitionResponse(BaseModel):
    task_definition: dict


class ListTaskDefinitionsRequest(BaseModel):
    family_prefix: str = None
    status: str = None
    sort: str = None
    max_results: int = None
    next_token: str = None


class ListTaskDefinitionsResponse(BaseModel):
    task_definitions: List[str]
