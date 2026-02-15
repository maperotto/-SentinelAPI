import asyncio
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from app.core.config import settings
from app.core.logger import setup_logger
from app.core.models import EndpointConfig, HealthCheckResult
from app.monitor.health_checker import HealthChecker
from app.notifier.discord import DiscordNotifier
from app.notifier.email import EmailNotifier
from app.notifier.telegram import TelegramNotifier

logger = setup_logger(__name__)
console = Console()


def load_endpoints(file_path: str = "endpoints.json") -> list[EndpointConfig]:
    config_file = Path(file_path)
    
    if not config_file.exists():
        logger.warning(f"Arquivo de configuração {file_path} não encontrado")
        return []
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        endpoints = [EndpointConfig(**endpoint) for endpoint in data]
        logger.info(f"Carregados {len(endpoints)} endpoints para monitoramento")
        return endpoints
        
    except Exception as e:
        logger.error(f"Erro ao carregar endpoints: {e}")
        return []


def display_results(results: list[HealthCheckResult]) -> None:
    table = Table(title="Status de Monitoramento")
    
    table.add_column("Endpoint", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold")
    table.add_column("Tempo (s)", justify="right")
    table.add_column("Status Code", justify="center")
    table.add_column("Erro", style="red")
    
    for result in results:
        status_color = {
            "healthy": "[green]HEALTHY[/green]",
            "degraded": "[yellow]DEGRADED[/yellow]",
            "down": "[red]DOWN[/red]"
        }
        
        table.add_row(
            result.endpoint,
            status_color.get(result.status, result.status),
            f"{result.response_time:.2f}",
            str(result.status_code) if result.status_code else "N/A",
            result.error_message or ""
        )
    
    console.print(table)


async def send_alerts(results: list[HealthCheckResult]) -> None:
    notifiers = [
        TelegramNotifier(),
        DiscordNotifier(),
        EmailNotifier()
    ]
    
    active_notifiers = [n for n in notifiers if n.is_configured()]
    
    if not active_notifiers:
        logger.info("Nenhum notificador configurado")
        return
    
    for result in results:
        if not result.is_healthy:
            tasks = [
                notifier.send_alert(result) 
                for notifier in active_notifiers 
                if notifier.should_alert(result)
            ]
            await asyncio.gather(*tasks)


async def monitor_loop(endpoints: list[EndpointConfig]) -> None:
    async with HealthChecker(max_retries=settings.max_retries) as checker:
        while True:
            try:
                console.print(f"\n[bold blue]Iniciando verificação de saúde...[/bold blue]")
                
                results = await checker.check_multiple(endpoints)
                display_results(results)
                
                await send_alerts(results)
                
                console.print(
                    f"\n[dim]Próxima verificação em {settings.monitor_interval}s...[/dim]"
                )
                await asyncio.sleep(settings.monitor_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoramento interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
                await asyncio.sleep(10)


def main() -> None:
    console.print("[bold green]🚀 SentinelAPI iniciado[/bold green]")
    logger.info("SentinelAPI iniciado")
    logger.info(f"Intervalo de monitoramento: {settings.monitor_interval}s")
    
    endpoints = load_endpoints()
    
    if not endpoints:
        logger.error("Nenhum endpoint configurado para monitoramento")
        return
    
    console.print(f"\n[cyan]Endpoints configurados: {len(endpoints)}[/cyan]")
    for endpoint in endpoints:
        console.print(f"  • {endpoint.name} - {endpoint.url}")
    
    try:
        asyncio.run(monitor_loop(endpoints))
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoramento encerrado[/yellow]")


if __name__ == "__main__":
    main()
