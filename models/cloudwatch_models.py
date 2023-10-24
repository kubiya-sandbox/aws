from pydantic import BaseModel
from typing import List


class CreateAlarmRequest(BaseModel):
    AlarmName: str
    ComparisonOperator: str
    EvaluationPeriods: int
    MetricName: str
    Namespace: str
    Period: int
    Statistic: str
    Threshold: float
    AlarmDescription: str = None
    ActionsEnabled: bool = None
    AlarmActions: List[str] = None


class CreateAlarmResponse(BaseModel):
    alarm_name: str


class DeleteAlarmRequest(BaseModel):
    alarm_name: str


class DeleteAlarmResponse(BaseModel):
    alarm_name: str


class DescribeAlarmsRequest(BaseModel):
    AlarmNames: List[str] = None


class DescribeAlarmsResponse(BaseModel):
    alarms: List[dict]


class PutMetricDataRequest(BaseModel):
    Namespace: str
    MetricData: List[dict]


class PutMetricDataResponse(BaseModel):
    pass


class GetMetricDataRequest(BaseModel):
    MetricDataQueries: List[dict]
    StartTime: str
    EndTime: str
    NextToken: str = None


class GetMetricDataResponse(BaseModel):
    metric_data: List[dict]


class ListMetricsRequest(BaseModel):
    Namespace: str
    MetricName: str = None
    Dimensions: List[dict] = None


class ListMetricsResponse(BaseModel):
    metrics: List[dict]
