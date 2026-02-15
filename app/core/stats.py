from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class MonitorStats:
    total_checks: int = 0
    healthy_count: int = 0
    degraded_count: int = 0
    down_count: int = 0
    average_response_time: float = 0.0
    last_check: str = ""


class StatsTracker:
    def __init__(self, stats_file: str = "monitor_stats.json"):
        self.stats_file = Path(stats_file)
        self.stats = self._load_stats()
    
    def _load_stats(self) -> MonitorStats:
        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r") as f:
                    data = json.load(f)
                return MonitorStats(**data)
            except Exception:
                pass
        return MonitorStats()
    
    def _save_stats(self) -> None:
        with open(self.stats_file, "w") as f:
            json.dump(self.stats.__dict__, f, indent=2)
    
    def update(self, results: list) -> None:
        if not results:
            return
        
        self.stats.total_checks += len(results)
        
        for result in results:
            if result.status.value == "healthy":
                self.stats.healthy_count += 1
            elif result.status.value == "degraded":
                self.stats.degraded_count += 1
            else:
                self.stats.down_count += 1
        
        avg_time = sum(r.response_time for r in results) / len(results)
        if self.stats.average_response_time == 0:
            self.stats.average_response_time = avg_time
        else:
            self.stats.average_response_time = (
                self.stats.average_response_time * 0.7 + avg_time * 0.3
            )
        
        self.stats.last_check = datetime.now().isoformat()
        self._save_stats()
    
    def get_uptime_percentage(self) -> float:
        if self.stats.total_checks == 0:
            return 0.0
        return (self.stats.healthy_count / self.stats.total_checks) * 100
