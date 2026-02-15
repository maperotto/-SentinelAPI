from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"


class EndpointConfig(BaseModel):
    name: str
    url: HttpUrl
    method: str = "GET"
    expected_status: int = 200
    timeout: int = 10
    
    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        allowed = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"]
        if v.upper() not in allowed:
            raise ValueError(f"Method must be one of {allowed}")
        return v.upper()


class HealthCheckResult(BaseModel):
    endpoint: str
    url: str
    status: HealthStatus
    response_time: float
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: datetime = datetime.now()
    
    @property
    def is_healthy(self) -> bool:
        return self.status == HealthStatus.HEALTHY
