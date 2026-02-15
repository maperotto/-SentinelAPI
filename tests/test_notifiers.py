from app.core.models import HealthCheckResult, HealthStatus
from app.notifier.discord import DiscordNotifier
from app.notifier.email import EmailNotifier
from app.notifier.telegram import TelegramNotifier


def test_telegram_notifier_not_configured():
    notifier = TelegramNotifier()
    notifier.bot_token = ""
    notifier.chat_id = ""
    
    assert not notifier.is_configured()


def test_discord_notifier_not_configured():
    notifier = DiscordNotifier()
    notifier.webhook_url = ""
    
    assert not notifier.is_configured()


def test_email_notifier_not_configured():
    notifier = EmailNotifier()
    notifier.smtp_user = ""
    notifier.smtp_password = ""
    
    assert not notifier.is_configured()


def test_notifier_should_alert_on_unhealthy():
    notifier = TelegramNotifier()
    
    result = HealthCheckResult(
        endpoint="Test",
        url="https://example.com",
        status=HealthStatus.DOWN,
        response_time=1.0,
        error_message="Error"
    )
    
    assert notifier.should_alert(result)


def test_notifier_should_not_alert_on_healthy():
    notifier = TelegramNotifier()
    
    result = HealthCheckResult(
        endpoint="Test",
        url="https://example.com",
        status=HealthStatus.HEALTHY,
        response_time=0.5,
        status_code=200
    )
    
    assert not notifier.should_alert(result)
