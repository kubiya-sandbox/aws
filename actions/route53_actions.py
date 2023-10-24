from ..models.route53_models import (
    ListHostedZonesListRequest,ListHostedZonesListResponse,
    CreateHostedZonesRequest,CreateHostedZonesResponse,
)

from ..main_store import store
from ..aws_wrapper import get_resource ,get_client


@store.kubiya_action()
def list_hosted_zones(request: ListHostedZonesListRequest) -> ListHostedZonesListResponse:
    """
    List hosted zones in Amazon Route 53.

    Args:
        request (ListHostedZonesListRequest): The request object containing any necessary parameters.
        ListHostedZonesListRequest:
            marker: Optional[str]
            max_items: Optional[str]
            delegation_set_id: Optional[str]

    Returns:
        ListHostedZonesListResponse: The response object containing the list of hosted zones.

    Raises:
        SomeException: This function may raise an exception if something goes wrong.
    """
    route53 = get_client("route53")
    response = route53.list_hosted_zones()
    return ListHostedZonesListResponse(message=response)

@store.kubiya_action()
def create_hosted_zone(request: CreateHostedZonesRequest) -> CreateHostedZonesResponse:

    route53 = get_client("route53")
    response = route53.create_hosted_zone(Name=request.name,
                                          CallerReference=request.caller_reference,
                                          HostedZoneConfig={"Comment":request.comment,
                                                            "PrivateZone":request.private_zone},
                                          VPC={"VPCRegion":request.vpc_region,
                                               "VPCId":request.vpc_id})

    return CreateHostedZonesResponse(response=response)
