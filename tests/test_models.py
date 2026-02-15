import pytest

from app.core.models import EndpointConfig, HealthCheckResult, HealthStatus


def test_endpoint_config_validation():
    config = EndpointConfig(
        name="Test API",
        url="https://api.example.com",
        method="GET",
        expected_status=200,
        timeout=5
    )
    
    assert config.name == "Test API"
    assert str(config.url) == "https://api.example.com/"
    assert config.method == "GET"


def test_endpoint_config_invalid_method():
    with pytest.raises(ValueError):
        EndpointConfig(
            name="Test",
            url="https://example.com",
            method="INVALID"
        )


def test_health_check_result_healthy():
    result = HealthCheckResult(
        endpoint="Test",
        url="https://example.com",
        status=HealthStatus.HEALTHY,
        response_time=0.5,
        status_code=200
    )
    
    assert result.is_healthy
    assert result.status == HealthStatus.HEALTHY


def test_health_check_result_down():
    result = HealthCheckResult(
        endpoint="Test",
        url="https://example.com",
        status=HealthStatus.DOWN,
        response_time=5.0,
        error_message="Connection timeout"
    )
    
    assert not result.is_healthy
    assert result.status == HealthStatus.DOWN
    assert result.error_message == "Connection timeout"
