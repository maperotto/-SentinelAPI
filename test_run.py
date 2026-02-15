import asyncio
from app.core.models import EndpointConfig, HealthStatus
from app.monitor.health_checker import HealthChecker


async def quick_test():
    test_endpoints = [
        EndpointConfig(
            name="Google",
            url="https://www.google.com",
            method="GET",
            expected_status=200,
            timeout=5
        ),
        EndpointConfig(
            name="GitHub API",
            url="https://api.github.com",
            method="GET",
            expected_status=200,
            timeout=10
        )
    ]
    
    print("Testando monitoramento de endpoints...\n")
    
    async with HealthChecker(max_retries=2) as checker:
        results = await checker.check_multiple(test_endpoints)
    
    for result in results:
        status_icon = "✓" if result.is_healthy else "✗"
        print(f"{status_icon} {result.endpoint}")
        print(f"  Status: {result.status.value}")
        print(f"  Tempo: {result.response_time:.2f}s")
        if result.error_message:
            print(f"  Erro: {result.error_message}")
        print()


if __name__ == "__main__":
    asyncio.run(quick_test())
