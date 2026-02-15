import httpx

from app.core.config import settings
from app.core.logger import setup_logger
from app.core.models import HealthCheckResult
from app.notifier.base import NotifierBase

logger = setup_logger(__name__)


class TelegramNotifier(NotifierBase):
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)
    
    async def send_alert(self, result: HealthCheckResult) -> bool:
        if not self.is_configured():
            logger.warning("Telegram não configurado. Ignorando alerta.")
            return False
        
        status_emoji = {
            "healthy": "✅",
            "degraded": "⚠️",
            "down": "🔴"
        }
        
        emoji = status_emoji.get(result.status, "❓")
        
        message = (
            f"{emoji} *Alerta SentinelAPI*\n\n"
            f"*Endpoint:* {result.endpoint}\n"
            f"*Status:* {result.status.upper()}\n"
            f"*URL:* {result.url}\n"
            f"*Tempo de resposta:* {result.response_time:.2f}s\n"
        )
        
        if result.status_code:
            message += f"*Status Code:* {result.status_code}\n"
        
        if result.error_message:
            message += f"*Erro:* {result.error_message}\n"
        
        message += f"\n_Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}_"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "Markdown"
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info(f"Alerta do Telegram enviado para {result.endpoint}")
                    return True
                else:
                    logger.error(f"Falha ao enviar alerta do Telegram: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Erro ao enviar alerta do Telegram: {e}")
            return False
