from typing import List
from ..models.ec2_models import (
    TerminateInstanceRequest,
    TerminateInstanceResponse,
    CreateInstanceRequest,
    CreateInstanceResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    SecurityGroup,
    ListUnusedSecurityGroupsRequest,
    ListUnusedSecurityGroupsResponse
)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def terminate_ec2_instance(request: TerminateInstanceRequest) -> TerminateInstanceResponse:
    """
    Terminates the specified EC2 instance.

    Args:
        request (TerminateInstanceRequest): The request containing the ID of the EC2 instance to terminate.

    Returns:
        TerminateInstanceResponse: The response containing a message indicating the termination of the instance.
    """
    ec2 = get_client("ec2")
    ec2.terminate_instances(InstanceIds=[request.instance_id])
    message = f'Instance {request.instance_id} termination initiated.'
    return TerminateInstanceResponse(message=message)


@store.kubiya_action()
def create_ec2_instance(request: CreateInstanceRequest) -> CreateInstanceResponse:
    """
    Creates a new EC2 instance.

    Args:
        request (CreateInstanceRequest): The request containing the details of the instance to create.

    Returns:
        CreateInstanceResponse: The response containing the details of the created instance.
    """
    ec2 = get_client("ec2")
    response = ec2.run_instances(
        ImageId=request.image_id,
        InstanceType=request.instance_type,
        MinCount=request.min_count,
        MaxCount=request.max_count,
    )
    instance_id = response["Instances"][0]["InstanceId"]
    return CreateInstanceResponse(instance_id=instance_id)


@store.kubiya_action()
def list_ec2_instances(request: ListInstancesRequest) -> ListInstancesResponse:
    """
    Lists EC2 instances based on the specified filters.

    Args:
        request (ListInstancesRequest): The request containing the filters.

    Returns:
        ListInstancesResponse: The response containing the list of instances.
    """
    ec2 = get_client("ec2")
    filters = []
    if request.instance_ids:
        filters.append({'Name': 'instance-id', 'Values': request.instance_ids})
    if request.instance_types:
        filters.append({'Name': 'instance-type', 'Values': request.instance_types})
    # Add more filters as needed...
    response = ec2.describe_instances(Filters=filters)
    instances = []
    for reservation in response["Reservations"]:
        instances.extend(reservation["Instances"])
    return ListInstancesResponse(instances=instances)


@store.kubiya_action()
def list_unused_security_groups(r: ListUnusedSecurityGroupsRequest) -> ListUnusedSecurityGroupsResponse:
    """
    Lists unused security groups in the specified region.

    Args:
        request (ListUnusedSecurityGroupsRequest): The request containing the region.

    Returns:
        ListUnusedSecurityGroupsResponse: The response containing the list of unused security groups.
    """
    ec2_client = get_client("ec2")

    # Get all EC2 instances
    instances = ec2_client.describe_instances()

    # # Get all security groups
    all_sgs = ec2_client.describe_security_groups()['SecurityGroups']

    # # Get all security groups associated with instances
    used_sg_ids = set()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance['SecurityGroups']:
                used_sg_ids.add(sg['GroupId'])

    # # Filter unused security groups
    unused_sgs = [sg for sg in all_sgs if sg['GroupId'] not in used_sg_ids]

    # Convert to list of SecurityGroup classes
    return ListUnusedSecurityGroupsResponse(
        unused=[SecurityGroup(id=sg['GroupId'], name=sg['GroupName']) for sg in unused_sgs])
