from ..models.s3_models import (
    S3MoveObjectRequest,
    S3MoveObjectResponse,
    S3CreateBucketRequest,
    S3CreateBucketResponse,
    S3DeleteBucketRequest,
    S3DeleteBucketResponse,
    S3ListBucketsRequest,
    S3ListBucketsResponse
)
from ..main_store import store
from ..aws_wrapper import get_client

from botocore.exceptions import NoCredentialsError


@store.kubiya_action()
def copy_object_to_s3(request: S3MoveObjectRequest) -> S3MoveObjectResponse:
    """
    Copies an object from one S3 bucket to another.

    Args:
        request (S3MoveObjectRequest): The request containing the details for the S3 object move.

    Returns:
        S3MoveObjectResponse: The response indicating the result of the object move.
    """
    s3 = get_client('s3')

    try:
        s3.copy_object(
            CopySource={'Bucket': request.source_bucket, 'Key': request.object_key},
            Bucket=request.destination_bucket,
            Key=request.object_key
        )

        message = f"Object '{request.object_key}' copied from '{request.source_bucket}' to '{request.destination_bucket}'."
        return S3MoveObjectResponse(message=message)
    except NoCredentialsError:
        message = "Credentials not available. Unable to move the object."
        return S3MoveObjectResponse(message=message)
    

@store.kubiya_action()
def create_s3_bucket(request: S3CreateBucketRequest) -> S3CreateBucketResponse:
    """
    Creates an S3 bucket.

    Args:
        request (S3CreateBucketRequest): The request containing the details for the S3 bucket creation.

    Returns:
        S3CreateBucketResponse: The response indicating the result of the bucket creation.
    """
    s3 = get_client('s3')

    try:
        s3.create_bucket(
            Bucket=request.bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': request.region
            }
        )

        message = f"Bucket '{request.bucket_name}' created in '{request.region}'."
        return S3CreateBucketResponse(message=message)
    except NoCredentialsError:
        message = "Credentials not available. Unable to create the bucket."
        return S3CreateBucketResponse(message=message)
    

@store.kubiya_action()
def delete_s3_bucket(request: S3DeleteBucketRequest) -> S3DeleteBucketResponse:
    """
    Deletes an S3 bucket.

    Args:
        request (S3DeleteBucketRequest): The request containing the details for the S3 bucket deletion.

    Returns:
        S3DeleteBucketResponse: The response indicating the result of the bucket deletion.
    """
    s3 = get_client('s3')

    try:
        s3.delete_bucket(
            Bucket=request.bucket_name
        )

        message = f"Bucket '{request.bucket_name}' deleted."
        return S3DeleteBucketResponse(message=message)
    except NoCredentialsError:
        message = "Credentials not available. Unable to delete the bucket."
        return S3DeleteBucketResponse(message=message)
    

@store.kubiya_action()
def list_s3_buckets(request: S3ListBucketsRequest) -> S3ListBucketsResponse:
    """
    Lists the S3 buckets.

    Args:
        request (S3ListBucketsRequest): The request containing the details for the S3 bucket listing.

    Returns:
        S3ListBucketsResponse: The response containing the list of buckets.
    """
    s3 = get_client('s3')

    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]

        return S3ListBucketsResponse(buckets=buckets)
    except NoCredentialsError:
        message = "Credentials not available. Unable to list the buckets."
        return S3ListBucketsResponse(message=message)