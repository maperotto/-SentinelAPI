import pytest

from app.core.models import EndpointConfig, HealthStatus
from app.monitor.health_checker import HealthChecker


@pytest.mark.asyncio
async def test_health_checker_healthy_endpoint():
    endpoint = EndpointConfig(
        name="GitHub",
        url="https://api.github.com",
        method="GET",
        expected_status=200,
        timeout=10
    )
    
    async with HealthChecker(max_retries=1) as checker:
        result = await checker.check_endpoint(endpoint)
    
    assert result.endpoint == "GitHub"
    assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]
    assert result.response_time > 0


@pytest.mark.asyncio
async def test_health_checker_invalid_url():
    endpoint = EndpointConfig(
        name="Invalid",
        url="https://this-domain-does-not-exist-12345.com",
        method="GET",
        expected_status=200,
        timeout=5
    )
    
    async with HealthChecker(max_retries=1) as checker:
        result = await checker.check_endpoint(endpoint)
    
    assert result.status == HealthStatus.DOWN
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_health_checker_multiple_endpoints():
    endpoints = [
        EndpointConfig(
            name="Google",
            url="https://www.google.com",
            method="GET",
            expected_status=200,
            timeout=5
        ),
        EndpointConfig(
            name="GitHub",
            url="https://api.github.com",
            method="GET",
            expected_status=200,
            timeout=5
        )
    ]
    
    async with HealthChecker(max_retries=1) as checker:
        results = await checker.check_multiple(endpoints)
    
    assert len(results) == 2
    assert all(r.response_time > 0 for r in results)
