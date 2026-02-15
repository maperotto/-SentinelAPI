import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logger import setup_logger
from app.core.models import HealthCheckResult
from app.notifier.base import NotifierBase

logger = setup_logger(__name__)


class EmailNotifier(NotifierBase):
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.alert_email = settings.alert_email
    
    def is_configured(self) -> bool:
        return bool(
            self.smtp_host and 
            self.smtp_user and 
            self.smtp_password and 
            self.alert_email
        )
    
    async def send_alert(self, result: HealthCheckResult) -> bool:
        if not self.is_configured():
            logger.warning("Email não configurado. Ignorando alerta.")
            return False
        
        subject = f"[SentinelAPI] Alerta: {result.endpoint} está {result.status.upper()}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: {'#28a745' if result.is_healthy else '#dc3545'};">
                Alerta do SentinelAPI
            </h2>
            <p><strong>Endpoint:</strong> {result.endpoint}</p>
            <p><strong>Status:</strong> <span style="color: {'#28a745' if result.is_healthy else '#dc3545'}; font-weight: bold;">{result.status.upper()}</span></p>
            <p><strong>URL:</strong> {result.url}</p>
            <p><strong>Tempo de Resposta:</strong> {result.response_time:.2f}s</p>
            {"<p><strong>Status Code:</strong> " + str(result.status_code) + "</p>" if result.status_code else ""}
            {"<p><strong>Erro:</strong> <span style='color: #dc3545;'>" + result.error_message + "</span></p>" if result.error_message else ""}
            <hr>
            <p style="font-size: 12px; color: #777;">
                Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </body>
        </html>
        """
        
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.smtp_user
            msg["To"] = self.alert_email
            
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Alerta de email enviado para {result.endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar alerta de email: {e}")
            return False
