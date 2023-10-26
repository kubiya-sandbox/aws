from pydantic import BaseModel

class S3MoveObjectRequest(BaseModel):
    source_bucket: str
    destination_bucket: str
    object_key: str

class S3MoveObjectResponse(BaseModel):
    message: str

class S3CreateBucketRequest(BaseModel):
    bucket_name: str
    region: str

class S3CreateBucketResponse(BaseModel):
    message: str

class S3DeleteBucketRequest(BaseModel):
    bucket_name: str

class S3DeleteBucketResponse(BaseModel):
    message: str

class S3DeleteObjectRequest(BaseModel):
    bucket_name: str
    object_key: str

class S3DeleteObjectResponse(BaseModel):
    message: str