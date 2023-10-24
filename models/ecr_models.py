from pydantic import BaseModel
from typing import List


class CreateRepositoryRequest(BaseModel):
    repository_name: str


class CreateRepositoryResponse(BaseModel):
    repository_name: str
    repository_arn: str


class DeleteRepositoryRequest(BaseModel):
    repository_name: str


class DeleteRepositoryResponse(BaseModel):
    repository_name: str


class DescribeRepositoriesRequest(BaseModel):
    repository_names: List[str] = None


class DescribeRepositoriesResponse(BaseModel):
    repositories: List[dict]


class ListImagesRequest(BaseModel):
    repository_name: str
    filter_tags: List[dict] = None
    max_results: int = None
    next_token: str = None


class ListImagesResponse(BaseModel):
    images: List[dict]


class FindImagesRequest(BaseModel):
    search_pattern: str


class FindImagesResponse(BaseModel):
    matched_images: List[dict]
