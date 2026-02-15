import json
from pathlib import Path

from app.core.config import settings
from app.core.logger import setup_logger
from app.core.models import EndpointConfig

logger = setup_logger(__name__)


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


def main() -> None:
    logger.info("SentinelAPI iniciado")
    logger.info(f"Intervalo de monitoramento: {settings.monitor_interval}s")
    
    endpoints = load_endpoints()
    
    if not endpoints:
        logger.error("Nenhum endpoint configurado para monitoramento")
        return
    
    for endpoint in endpoints:
        logger.info(f"Endpoint configurado: {endpoint.name} - {endpoint.url}")


if __name__ == "__main__":
    main()
