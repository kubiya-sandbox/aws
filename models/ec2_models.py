from pydantic import BaseModel
from typing import List, Optional


class TerminateInstanceRequest(BaseModel):
    instance_id: str


class TerminateInstanceResponse(BaseModel):
    message: str


class CreateInstanceRequest(BaseModel):
    image_id: str
    instance_type: str
    min_count: int
    max_count: int


class CreateInstanceResponse(BaseModel):
    instance_id: str


class ListInstancesRequest(BaseModel):
    instance_ids: List[str] = None
    instance_types: List[str] = None


class ListInstancesResponse(BaseModel):
    instances: List[dict]

class SecurityGroup(BaseModel):
    id: str = None
    name: str = None
class ListUnusedSecurityGroupsRequest(BaseModel):
    pass
        
class ListUnusedSecurityGroupsResponse(BaseModel):
    unused: List[SecurityGroup]