from ..models.ecs_models import (
    RegisterTaskDefinitionRequest,
    RegisterTaskDefinitionResponse,
    DeregisterTaskDefinitionRequest,
    DeregisterTaskDefinitionResponse,
    DescribeTaskDefinitionRequest,
    DescribeTaskDefinitionResponse,
    ListTaskDefinitionsRequest,
    ListTaskDefinitionsResponse,
)
from ..main_store import store
from ..aws_wrapper import get_client, get_client
from botocore.exceptions import ClientError


@store.kubiya_action()
def register_task_definition(request: RegisterTaskDefinitionRequest) -> RegisterTaskDefinitionResponse:
    """
    Registers a new task definition in ECS.

    Args:
        request (RegisterTaskDefinitionRequest): The request containing the details of the task definition.

    Returns:
        RegisterTaskDefinitionResponse: The response containing the details of the registered task definition.
    """
    ecs = get_client("ecs")
    response = ecs.register_task_definition(**request.dict(exclude_none=True))
    task_definition = response["taskDefinition"]
    return RegisterTaskDefinitionResponse(task_definition=task_definition)


@store.kubiya_action()
def deregister_task_definition(request: DeregisterTaskDefinitionRequest) -> DeregisterTaskDefinitionResponse:
    """
    Deregisters a task definition in ECS.

    Args:
        request (DeregisterTaskDefinitionRequest): The request containing the ARN of the task definition.

    Returns:
        DeregisterTaskDefinitionResponse: The response indicating the deregistration of the task definition.
    """
    ecs = get_client("ecs")

    try:
        response = ecs.deregister_task_definition(taskDefinition=request.task_definition_arn)
        return DeregisterTaskDefinitionResponse(task_definition_arn=request.task_definition_arn)
    except ClientError as e:
        error_message = f"An error occurred while deregistering the task definition: {str(e)}"
        return DeregisterTaskDefinitionResponse(task_definition_arn=request.task_definition_arn, error_message=error_message)


@store.kubiya_action()
def describe_task_definition(request: DescribeTaskDefinitionRequest) -> DescribeTaskDefinitionResponse:
    """
    Describes a task definition in ECS.

    Args:
        request (DescribeTaskDefinitionRequest): The request containing the ARN of the task definition.

    Returns:
        DescribeTaskDefinitionResponse: The response containing the details of the task definition.
    """
    ecs = get_client("ecs")
    response = ecs.describe_task_definition(taskDefinition=request.task_definition_arn)
    task_definition = response["taskDefinition"]
    return DescribeTaskDefinitionResponse(task_definition=task_definition)


@store.kubiya_action()
def list_task_definitions(request: ListTaskDefinitionsRequest) -> ListTaskDefinitionsResponse:
    """
    Lists task definitions in ECS based on the specified filters.

    Args:
        request (ListTaskDefinitionsRequest): The request containing the filters.

    Returns:
        ListTaskDefinitionsResponse: The response containing the list of task definitions.
    """
    ecs = get_client("ecs")
    response = ecs.list_task_definitions(
        familyPrefix=request.family_prefix,
        status=request.status,
        sort=request.sort,
        maxResults=request.max_results,
        nextToken=request.next_token,
    )
    task_definitions = response["taskDefinitionArns"]
    return ListTaskDefinitionsResponse(task_definitions=task_definitions)