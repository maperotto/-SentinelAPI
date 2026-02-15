from typing import Optional
from pydantic import BaseModel


class AlertConfig(BaseModel):
    enabled: bool = True
    notify_on_recovery: bool = True
    min_failures_before_alert: int = 1
    alert_cooldown_minutes: int = 5


class EndpointAlertState:
    def __init__(self):
        self.consecutive_failures = 0
        self.last_alert_time: Optional[float] = None
        self.was_down = False
    
    def should_alert(self, config: AlertConfig, current_time: float) -> bool:
        if not config.enabled:
            return False
        
        if config.alert_cooldown_minutes > 0 and self.last_alert_time:
            cooldown_seconds = config.alert_cooldown_minutes * 60
            if current_time - self.last_alert_time < cooldown_seconds:
                return False
        
        if self.consecutive_failures >= config.min_failures_before_alert:
            self.last_alert_time = current_time
            return True
        
        return False
    
    def should_notify_recovery(self, config: AlertConfig) -> bool:
        return config.notify_on_recovery and self.was_down
    
    def record_failure(self) -> None:
        self.consecutive_failures += 1
        self.was_down = True
    
    def record_success(self) -> None:
        self.consecutive_failures = 0
        self.was_down = False
