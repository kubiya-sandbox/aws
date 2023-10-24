from pydantic import BaseModel
from typing import List, Optional


class CreateClusterRequest(BaseModel):
    name: str
    roleArn: str
    version: str = None
    resourcesVpcConfig: dict = None
    logging: Optional[dict] = None


class CreateClusterResponse(BaseModel):
    cluster_name: str


class DeleteClusterRequest(BaseModel):
    cluster_name: str


class DeleteClusterResponse(BaseModel):
    cluster_name: str


class DescribeClusterRequest(BaseModel):
    cluster_name: str


class DescribeClusterResponse(BaseModel):
    cluster: dict


class ListClustersRequest(BaseModel):
    max_results: int = None
    next_token: str = None


class ListClustersResponse(BaseModel):
    clusters: List[str]
