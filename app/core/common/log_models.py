from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional, Mapping, Any
from pydantic import BaseModel, Field, field_serializer


class LogTypeOptions(Enum):
    """
    Enum for the different types of log messages that can be sent to runningman

    Attributes:
        SUCCESS (str): The success log type
        ERROR (str): The error log type
    """
    SUCCESS: str = 'SUCCESS'
    ERROR: str = 'ERROR'


class SentryLog(BaseModel):
    """
    Model for a log message to be sent to the runningman service

    Attributes:
        timestamp (datetime): The timestamp of the log message
        process_name (AllowedProcessNames): The name of the process that generated the log message
        log_type (LogTypeOptions): The type of log message
        payload (GenericPayload): The payload of the log message
        data_id (str): The data id of the log message
        company (str): The company of the log message
        retailer (str): The retailer of the log message
        error (str): The error message of the log message
    """
    timestamp: datetime = Field(default_factory=datetime.now)
    process_name: str
    log_type: LogTypeOptions
    payload: Mapping[str, Any] = Field(default_factory=dict)
    data_id: str = Field(default_factory=lambda: str(uuid4()))
    company: str
    retailer: str
    error: Optional[str]

    @field_serializer('timestamp')
    def serialize_timestamp(self, timestamp: datetime) -> str:
        """
        Serialize the timestamp of the log message
        """
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @field_serializer('data_id')
    def serialize_data_id(self, data_id: UUID) -> str:
        """
        Serialize the data id of the log message
        """
        return str(data_id)

    @field_serializer('log_type')
    def serialize_log_type(self, log_type: LogTypeOptions) -> str:
        """
        Serialize the log type of the log message
        """
        return log_type.value.lower()
