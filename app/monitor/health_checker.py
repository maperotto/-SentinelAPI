import asyncio
from time import time
from typing import Optional

import httpx

from app.core.logger import setup_logger
from app.core.models import EndpointConfig, HealthCheckResult, HealthStatus

logger = setup_logger(__name__)


class HealthChecker:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self) -> "HealthChecker":
        self.client = httpx.AsyncClient(follow_redirects=True)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.client:
            await self.client.aclose()
    
    async def check_endpoint(self, endpoint: EndpointConfig) -> HealthCheckResult:
        if not self.client:
            raise RuntimeError("HealthChecker deve ser usado como context manager")
        
        start_time = time()
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(
                    method=endpoint.method,
                    url=str(endpoint.url),
                    timeout=endpoint.timeout
                )
                
                elapsed = time() - start_time
                
                if response.status_code == endpoint.expected_status:
                    logger.info(
                        f"{endpoint.name}: HEALTHY "
                        f"(status={response.status_code}, time={elapsed:.2f}s)"
                    )
                    return HealthCheckResult(
                        endpoint=endpoint.name,
                        url=str(endpoint.url),
                        status=HealthStatus.HEALTHY,
                        response_time=elapsed,
                        status_code=response.status_code
                    )
                else:
                    logger.warning(
                        f"{endpoint.name}: DEGRADED "
                        f"(esperado={endpoint.expected_status}, "
                        f"recebido={response.status_code})"
                    )
                    return HealthCheckResult(
                        endpoint=endpoint.name,
                        url=str(endpoint.url),
                        status=HealthStatus.DEGRADED,
                        response_time=elapsed,
                        status_code=response.status_code,
                        error_message=f"Status code inesperado: {response.status_code}"
                    )
                    
            except httpx.TimeoutException as e:
                last_error = f"Timeout após {endpoint.timeout}s"
                logger.warning(f"{endpoint.name}: Tentativa {attempt + 1} - {last_error}")
                
            except httpx.RequestError as e:
                last_error = f"Erro de requisição: {str(e)}"
                logger.warning(f"{endpoint.name}: Tentativa {attempt + 1} - {last_error}")
            
            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)
        
        elapsed = time() - start_time
        logger.error(f"{endpoint.name}: DOWN após {self.max_retries} tentativas")
        
        return HealthCheckResult(
            endpoint=endpoint.name,
            url=str(endpoint.url),
            status=HealthStatus.DOWN,
            response_time=elapsed,
            error_message=last_error or "Falha desconhecida"
        )
    
    async def check_multiple(
        self, endpoints: list[EndpointConfig]
    ) -> list[HealthCheckResult]:
        tasks = [self.check_endpoint(endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)
