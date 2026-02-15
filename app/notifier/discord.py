import httpx

from app.core.config import settings
from app.core.logger import setup_logger
from app.core.models import HealthCheckResult
from app.notifier.base import NotifierBase

logger = setup_logger(__name__)


class DiscordNotifier(NotifierBase):
    def __init__(self):
        self.webhook_url = settings.discord_webhook_url
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url)
    
    async def send_alert(self, result: HealthCheckResult) -> bool:
        if not self.is_configured():
            logger.warning("Discord não configurado. Ignorando alerta.")
            return False
        
        color_map = {
            "healthy": 0x00FF00,
            "degraded": 0xFFA500,
            "down": 0xFF0000
        }
        
        color = color_map.get(result.status, 0x808080)
        
        embed = {
            "title": f"Alerta: {result.endpoint}",
            "description": f"Status do endpoint alterado para **{result.status.upper()}**",
            "color": color,
            "fields": [
                {
                    "name": "URL",
                    "value": result.url,
                    "inline": False
                },
                {
                    "name": "Tempo de Resposta",
                    "value": f"{result.response_time:.2f}s",
                    "inline": True
                }
            ],
            "timestamp": result.timestamp.isoformat(),
            "footer": {
                "text": "SentinelAPI Monitor"
            }
        }
        
        if result.status_code:
            embed["fields"].append({
                "name": "Status Code",
                "value": str(result.status_code),
                "inline": True
            })
        
        if result.error_message:
            embed["fields"].append({
                "name": "Erro",
                "value": result.error_message,
                "inline": False
            })
        
        payload = {
            "embeds": [embed]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code in [200, 204]:
                    logger.info(f"Alerta do Discord enviado para {result.endpoint}")
                    return True
                else:
                    logger.error(f"Falha ao enviar alerta do Discord: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"Erro ao enviar alerta do Discord: {e}")
            return False
