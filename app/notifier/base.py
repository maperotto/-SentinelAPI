from abc import ABC, abstractmethod

from app.core.models import HealthCheckResult


class NotifierBase(ABC):
    @abstractmethod
    async def send_alert(self, result: HealthCheckResult) -> bool:
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        pass
    
    def should_alert(self, result: HealthCheckResult) -> bool:
        return not result.is_healthy
