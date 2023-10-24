from ..models.ecr_models import (
    CreateRepositoryRequest,
    CreateRepositoryResponse,
    DeleteRepositoryRequest,
    DeleteRepositoryResponse,
    DescribeRepositoriesRequest,
    DescribeRepositoriesResponse,
    ListImagesRequest,
    ListImagesResponse,
    FindImagesRequest,
    FindImagesResponse,
)
from ..main_store import store
from ..aws_wrapper import get_client

@store.kubiya_action()
def create_repository(request: CreateRepositoryRequest) -> CreateRepositoryResponse:
    """
    Creates a new ECR repository.

    Args:
        request (CreateRepositoryRequest): The request containing the details of the repository to create.

    Returns:
        CreateRepositoryResponse: The response containing the details of the created repository.
    """
    ecr = get_client("ecr")
    response = ecr.create_repository(repositoryName=request.repository_name)
    repository_arn = response["repository"]["repositoryArn"]
    return CreateRepositoryResponse(repository_name=request.repository_name, repository_arn=repository_arn)


@store.kubiya_action()
def delete_repository(request: DeleteRepositoryRequest) -> DeleteRepositoryResponse:
    """
    Deletes an ECR repository.

    Args:
        request (DeleteRepositoryRequest): The request containing the name of the repository to delete.

    Returns:
        DeleteRepositoryResponse: The response indicating the deletion of the repository.
    """
    ecr = get_client("ecr")
    response = ecr.delete_repository(repositoryName=request.repository_name)
    return DeleteRepositoryResponse(repository_name=request.repository_name)


@store.kubiya_action()
def describe_repositories(request: DescribeRepositoriesRequest) -> DescribeRepositoriesResponse:
    """
    Describes ECR repositories based on the specified filters.

    Args:
        request (DescribeRepositoriesRequest): The request containing the filters.

    Returns:
        DescribeRepositoriesResponse: The response containing the list of repositories.
    """
    ecr = get_client("ecr")
    response = ecr.describe_repositories(repositoryNames=request.repository_names)
    repositories = response["repositories"]
    return DescribeRepositoriesResponse(repositories=repositories)


@store.kubiya_action()
def list_images(request: ListImagesRequest) -> ListImagesResponse:
    """
    Lists images in an ECR repository based on the specified filters.

    Args:
        request (ListImagesRequest): The request containing the details of the repository and filters.

    Returns:
        ListImagesResponse: The response containing the list of images.
    """
    ecr = get_client("ecr")
    response = ecr.list_images(
        repositoryName=request.repository_name,
        filterTags=request.filter_tags,
        maxResults=request.max_results,
        nextToken=request.next_token,
    )
    images = response["imageIds"]
    return ListImagesResponse(images=images)


@store.kubiya_action()
def find_images(request: FindImagesRequest) -> FindImagesResponse:
    """
    Finds images in ECR repositories based on a search pattern.

    Args:
        request (FindImagesRequest): The request containing the search pattern.

    Returns:
        FindImagesResponse: The response containing the list of matched images.
    """
    ecr = get_client("ecr")
    response = ecr.describe_repositories()
    repositories = response["repositories"]
    matched_images = []

    for repository in repositories:
        repository_name = repository["repositoryName"]
        images_response = ecr.list_images(repositoryName=repository_name)
        images = images_response["imageIds"]

        for image in images:
            image_tag = image.get("imageTag")
            if image_tag and request.search_pattern in image_tag:
                matched_images.append({
                    "repositoryName": repository_name,
                    "imageDigest": image["imageDigest"],
                    "imageTag": image_tag,
                })

    return FindImagesResponse(matched_images=matched_images)