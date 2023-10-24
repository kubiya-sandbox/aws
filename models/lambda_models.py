from pydantic import BaseModel
from typing import List


class CreateFunctionRequest(BaseModel):
    FunctionName: str
    Runtime: str
    Role: str
    Handler: str
    Code: dict
    Description: str = None
    Timeout: int = None
    MemorySize: int = None
    Environment: dict = None


class CreateFunctionResponse(BaseModel):
    function_name: str


class DeleteFunctionRequest(BaseModel):
    function_name: str


class DeleteFunctionResponse(BaseModel):
    function_name: str


class GetFunctionRequest(BaseModel):
    function_name: str


class GetFunctionResponse(BaseModel):
    function: dict


class ListFunctionsRequest(BaseModel):
    max_results: int = None


class ListFunctionsResponse(BaseModel):
    functions: List[str]
