from ..models.iam_models import (
    CreateUserRequest,
    CreateUserResponse,
    DeleteUserRequest,
    DeleteUserResponse,
    ListUsersRequest,
    ListUsersResponse,
    CreateAccessKeyRequest,
    CreateAccessKeyResponse,
    ListAccessKeysRequest,
    ListAccessKeysResponse,
    S3AccessRequest,
    S3AccessResponse
)
from ..main_store import store
from ..aws_wrapper import get_resource, get_client
import json


@store.kubiya_action()
def create_user(request: CreateUserRequest) -> CreateUserResponse:
    """
    Creates a new IAM user.

    Args:
        request (CreateUserRequest): The request containing the details of the user to create.

    Returns:
        CreateUserResponse: The response containing the details of the created user.
    """
    iam = get_resource("iam")
    response = iam.create_user(UserName=request.username)
    user_arn = response["User"]["Arn"]
    return CreateUserResponse(username=request.username, arn=user_arn)


@store.kubiya_action()
def delete_user(request: DeleteUserRequest) -> DeleteUserResponse:
    """
    Deletes an IAM user.

    Args:
        request (DeleteUserRequest): The request containing the username of the user to delete.

    Returns:
        DeleteUserResponse: The response indicating the deletion of the user.
    """
    iam = get_client("iam")
    response = iam.delete_user(UserName=request.username)
    return DeleteUserResponse(username=request.username)


@store.kubiya_action()
def list_users(request: ListUsersRequest) -> ListUsersResponse:
    """
    Lists IAM users based on the specified filters.

    Args:
        request (ListUsersRequest): The request containing the filters.

    Returns:
        ListUsersResponse: The response containing the list of users.
    """
    iam = get_client("iam")
    users = []
    if request.usernames:
        for username in request.usernames:
            user = iam.get_user(UserName=username)["User"]
            users.append(user)
    else:
        users = iam.list_users()["Users"]
    return ListUsersResponse(users=users)


@store.kubiya_action()
def create_access_key(request: CreateAccessKeyRequest) -> CreateAccessKeyResponse:
    """
    Creates a new access key for an IAM user.

    Args:
        request (CreateAccessKeyRequest): The request containing the username of the user.

    Returns:
        CreateAccessKeyResponse: The response containing the details of the created access key.
    """
    iam = get_client("iam")
    response = iam.create_access_key(UserName=request.username)
    access_key = response["AccessKey"]
    return CreateAccessKeyResponse(
        username=request.username,
        access_key_id=access_key["AccessKeyId"],
        secret_access_key=access_key["SecretAccessKey"],
    )


@store.kubiya_action()
def list_access_keys(request: ListAccessKeysRequest) -> ListAccessKeysResponse:
    """
    Lists access keys for an IAM user.

    Args:
        request (ListAccessKeysRequest): The request containing the username of the user.

    Returns:
        ListAccessKeysResponse: The response containing the list of access keys.
    """
    iam = get_client("iam")
    response = iam.list_access_keys(UserName=request.username)
    access_keys = response["AccessKeyMetadata"]
    return ListAccessKeysResponse(access_keys=access_keys)


@store.kubiya_action()
def grant_s3_access(request: S3AccessRequest) -> S3AccessResponse:
    """
    Grants S3 access for an IAM user.

    Args:
        request (S3AccessRequest): The request containing the details of the S3 access.

    Returns:
        S3AccessResponse: The response indicating the result of the S3 access request.
    """
    s3 = get_client('s3')
    bucket_name = request.bucket_name

    if request.permissions == "read-only":
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::<account-id>:user/{request.user_name}"
                    },
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        message = f"Read permission granted for {request.user_name} on {bucket_name}"
    if request.permissions == "read-write":
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::<account-id>:user/{request.user_name}"
                    },
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        message = f"Read and write permissions granted for {request.user_name} on {bucket_name}"

    return S3AccessResponse(message=message)
