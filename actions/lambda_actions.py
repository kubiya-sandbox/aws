from ..models.lambda_models import (
    CreateFunctionRequest,
    CreateFunctionResponse,
    DeleteFunctionRequest,
    DeleteFunctionResponse,
    GetFunctionRequest,
    GetFunctionResponse,
    ListFunctionsRequest,
    ListFunctionsResponse,
)
from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def create_function(request: CreateFunctionRequest) -> CreateFunctionResponse:
    """
    Creates a new AWS Lambda function.

    Args:
        request (CreateFunctionRequest): The request containing the details of the function to create.

    Returns:
        CreateFunctionResponse: The response containing the details of the created function.
    """
    lambda_client = get_client("lambda")
    response = lambda_client.create_function(**request.dict(exclude_none=True))
    function_name = response["FunctionName"]
    return CreateFunctionResponse(function_name=function_name)


@store.kubiya_action()
def delete_function(request: DeleteFunctionRequest) -> DeleteFunctionResponse:
    """
    Deletes an AWS Lambda function.

    Args:
        request (DeleteFunctionRequest): The request containing the name of the function to delete.

    Returns:
        DeleteFunctionResponse: The response indicating the deletion of the function.
    """
    lambda_client = get_client("lambda")
    response = lambda_client.delete_function(FunctionName=request.function_name)
    return DeleteFunctionResponse(function_name=request.function_name)


@store.kubiya_action()
def get_function(request: GetFunctionRequest) -> GetFunctionResponse:
    """
    Retrieves the configuration information of an AWS Lambda function.

    Args:
        request (GetFunctionRequest): The request containing the name of the function.

    Returns:
        GetFunctionResponse: The response containing the details of the function.
    """
    lambda_client = get_client("lambda")
    response = lambda_client.get_function(FunctionName=request.function_name)
    function = response["Configuration"]
    return GetFunctionResponse(function=function)


@store.kubiya_action()
def list_functions(request: ListFunctionsRequest) -> ListFunctionsResponse:
    """
    Lists the AWS Lambda functions in the specified region.

    Args:
        request (ListFunctionsRequest): The request containing the optional filters.

    Returns:
        ListFunctionsResponse: The response containing the list of function names.
    """
    lambda_client = get_client("lambda")
    response = lambda_client.list_functions()
    functions = [function["FunctionName"] for function in response["Functions"]]
    return ListFunctionsResponse(functions=functions)
