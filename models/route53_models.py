from pydantic import BaseModel
from typing import List , Optional


class ListHostedZonesListRequest(BaseModel):
    marker: Optional[str]
    max_items: Optional[str]
    delegation_set_id: Optional[str]

class ListHostedZonesListResponse(BaseModel):
    message: dict

class CreateHostedZonesRequest(BaseModel):
    name: str
    caller_reference: str
    vpc_id: Optional[str]
    vpc_region: Optional[str]
    comment: Optional[str]
    private_zone: Optional[bool]

class CreateHostedZonesResponse(BaseModel):
    response: dict