from ..models.cloudwatch_models import (
    CreateAlarmRequest,
    CreateAlarmResponse,
    DeleteAlarmRequest,
    DeleteAlarmResponse,
    DescribeAlarmsRequest,
    DescribeAlarmsResponse,
    PutMetricDataRequest,
    PutMetricDataResponse,
    GetMetricDataRequest,
    GetMetricDataResponse,
    ListMetricsRequest,
    ListMetricsResponse,
)

from ..main_store import store
from ..aws_wrapper import get_client


@store.kubiya_action()
def create_alarm(request: CreateAlarmRequest) -> CreateAlarmResponse:
    """
    Creates a new CloudWatch alarm.

    Args:
        request (CreateAlarmRequest): The request containing the details of the alarm to create.

    Returns:
        CreateAlarmResponse: The response containing the details of the created alarm.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.put_metric_alarm(**request.dict(exclude_none=True))
    alarm_name = response["AlarmName"]
    return CreateAlarmResponse(alarm_name=alarm_name)


@store.kubiya_action()
def delete_alarm(request: DeleteAlarmRequest) -> DeleteAlarmResponse:
    """
    Deletes a CloudWatch alarm.

    Args:
        request (DeleteAlarmRequest): The request containing the name of the alarm to delete.

    Returns:
        DeleteAlarmResponse: The response indicating the deletion of the alarm.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.delete_alarms(AlarmNames=[request.alarm_name])
    return DeleteAlarmResponse(alarm_name=request.alarm_name)


@store.kubiya_action()
def describe_alarms(request: DescribeAlarmsRequest) -> DescribeAlarmsResponse:
    """
    Describes CloudWatch alarms based on the specified filters.

    Args:
        request (DescribeAlarmsRequest): The request containing the filters.

    Returns:
        DescribeAlarmsResponse: The response containing the list of alarms.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.describe_alarms(**request.dict(exclude_none=True))
    alarms = response["MetricAlarms"]
    return DescribeAlarmsResponse(alarms=alarms)


@store.kubiya_action()
def put_metric_data(request: PutMetricDataRequest) -> PutMetricDataResponse:
    """
    Publishes metric data to CloudWatch.

    Args:
        request (PutMetricDataRequest): The request containing the metric data to publish.

    Returns:
        PutMetricDataResponse: The response indicating the result of publishing the metric data.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.put_metric_data(**request.dict(exclude_none=True))
    return PutMetricDataResponse()


@store.kubiya_action()
def get_metric_data(request: GetMetricDataRequest) -> GetMetricDataResponse:
    """
    Retrieves metric data from CloudWatch.

    Args:
        request (GetMetricDataRequest): The request containing the details of the metric data to retrieve.

    Returns:
        GetMetricDataResponse: The response containing the retrieved metric data.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.get_metric_data(**request.dict(exclude_none=True))
    metric_data = response["MetricDataResults"]
    return GetMetricDataResponse(metric_data=metric_data)


@store.kubiya_action()
def list_metrics(request: ListMetricsRequest) -> ListMetricsResponse:
    """
    Lists the CloudWatch metrics based on the specified filters.

    Args:
        request (ListMetricsRequest): The request containing the filters.

    Returns:
        ListMetricsResponse: The response containing the list of metrics.
    """
    cloudwatch = get_client("cloudwatch")
    response = cloudwatch.list_metrics(**request.dict(exclude_none=True))
    metrics = response["Metrics"]
    return ListMetricsResponse(metrics=metrics)
