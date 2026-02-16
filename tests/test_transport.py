"""Tests for Transport and AsyncTransport error handling."""
import pytest
import respx

from payelink_agent_search.config import ClientConfig
from payelink_agent_search.errors import (
    HttpStatusError,
    InvalidResponseError,
)
from payelink_agent_search.transport import AsyncTransport, Transport


@respx.mock
def test_transport_http_4xx_raises_http_status_error():
    """Transport raises HttpStatusError on 4xx/5xx."""
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(403, text="Forbidden")
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = Transport(config)

    with pytest.raises(HttpStatusError) as exc_info:
        transport.post_json("/v1/agents/search", {"query": "test"})
    assert exc_info.value.status_code == 403
    transport.close()


@respx.mock
def test_transport_non_dict_response_raises_invalid_response():
    """Transport raises InvalidResponseError when response is not a dict."""
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=["array", "not", "object"])
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = Transport(config)

    with pytest.raises(InvalidResponseError):
        transport.post_json("/v1/agents/search", {"query": "test"})
    transport.close()


@respx.mock
def test_transport_invalid_json_body_raises_invalid_response():
    """Transport raises InvalidResponseError when body is not valid JSON."""
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(200, content=b"not json at all")
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = Transport(config)

    with pytest.raises(InvalidResponseError):
        transport.post_json("/v1/agents/search", {"query": "test"})
    transport.close()


@respx.mock
def test_transport_success_returns_dict():
    """Transport returns parsed JSON dict on success."""
    payload = {"success": True, "data": []}
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=payload)
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = Transport(config)

    result = transport.post_json("/v1/agents/search", {"query": "test"})
    assert result == payload
    transport.close()


@respx.mock
def test_transport_sets_auth_header_when_api_key():
    """Transport adds Bearer header when api_key is set."""
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json={"success": True, "data": []})
    )
    config = ClientConfig(
        base_url="https://api.example.com",
        retries=0,
        api_key="secret",
    )
    transport = Transport(config)

    transport.post_json("/v1/agents/search", {"query": "test"})

    request = respx.calls.last.request
    assert request.headers.get("Authorization") == "Bearer secret"
    transport.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_transport_http_error():
    """AsyncTransport raises HttpStatusError on 4xx."""
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(404, text="Not Found")
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = AsyncTransport(config)

    with pytest.raises(HttpStatusError) as exc_info:
        await transport.post_json("/v1/agents/search", {"query": "test"})
    assert exc_info.value.status_code == 404
    await transport.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_transport_success():
    """AsyncTransport returns dict on success (async parity)."""
    payload = {"success": True, "message": "OK", "data": []}
    respx.post("https://api.example.com/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=payload)
    )
    config = ClientConfig(base_url="https://api.example.com", retries=0)
    transport = AsyncTransport(config)

    result = await transport.post_json("/v1/agents/search", {"query": "test"})
    assert result == payload
    await transport.close()
