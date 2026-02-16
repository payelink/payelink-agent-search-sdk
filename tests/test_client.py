"""Tests for sync and async Agent Search clients."""
import json

import pytest
import respx

from payelink_agent_search import AgentSearchClient, AsyncAgentSearchClient
from payelink_agent_search.config import ClientConfig
from payelink_agent_search.errors import HttpStatusError, InvalidResponseError, SdkError


@respx.mock
def test_search_success(client_config, sample_search_response):
    """Success path: valid query returns agents."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=sample_search_response)
    )
    config = ClientConfig(
        base_url="https://api.payelink.example",
        retries=1,
        api_key="test-key",
    )
    client = AgentSearchClient(api_key="test-key")
    # Override transport config to use our base_url for respx
    client._config = config
    client._transport._config = config
    client._transport._client = client._transport._client  # keep same client

    # Build a new transport with test config so request goes to mocked URL
    from payelink_agent_search.transport import Transport

    client._transport = Transport(config)

    response = client.search("Convert USD to KES")

    assert response.success is True
    assert len(response.agents) == 2
    assert response.agents[0].agent_name == "Currency Converter"
    assert response.agents[1].agent_name == "Budget Planner"
    client.close()


@respx.mock
def test_search_success_minimal_payload(client_config):
    """Success path: API returns empty agent list."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(
            200,
            json={"success": True, "data": [], "message": "Found 0 agent(s)"},
        )
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    client = AgentSearchClient(api_key="skip")
    client._config = config
    from payelink_agent_search.transport import Transport

    client._transport = Transport(config)

    response = client.search("nonexistent intent")

    assert response.success is True
    assert len(response.agents) == 0
    client.close()


@respx.mock
def test_search_http_error(client_config):
    """Failure path: API returns 401."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(401, text="Unauthorized")
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    client = AgentSearchClient(api_key="bad-key")
    client._config = config
    from payelink_agent_search.transport import Transport

    client._transport = Transport(config)

    with pytest.raises(HttpStatusError) as exc_info:
        client.search("test")
    assert exc_info.value.status_code == 401
    client.close()


@respx.mock
def test_search_invalid_json(client_config):
    """Failure path: API returns non-JSON body."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(200, content=b"not json")
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    client = AgentSearchClient(api_key="test")
    client._config = config
    from payelink_agent_search.transport import Transport

    client._transport = Transport(config)

    with pytest.raises(InvalidResponseError):
        client.search("test")
    client.close()


@respx.mock
def test_search_filters_passed(client_config, sample_search_response):
    """Request payload includes filters (max_result, country, allowed_url)."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=sample_search_response)
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    client = AgentSearchClient(api_key="test")
    client._config = config
    from payelink_agent_search.transport import Transport

    client._transport = Transport(config)

    client.search(
        "finance",
        max_result=5,
        country="KE",
        allowed_url=["https://org.example.com"],
    )

    request = respx.calls.last.request
    body = json.loads(request.content)
    assert body["query"] == "finance"
    assert body["max_result"] == 5
    assert body["country"] == "KE"
    assert body["allowed_url"] == ["https://org.example.com"]
    client.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_search_success(client_config, sample_search_response):
    """Async client: success path."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(200, json=sample_search_response)
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    async with AsyncAgentSearchClient(api_key="test") as client:
        client._config = config
        from payelink_agent_search.transport import AsyncTransport

        client._transport = AsyncTransport(config)

        response = await client.search("translation agent")
        assert response.success is True
        assert len(response.agents) == 2


@pytest.mark.asyncio
@respx.mock
async def test_async_search_http_error(client_config):
    """Async client: HTTP error raises SdkError."""
    respx.post("https://api.payelink.example/v1/agents/search").mock(
        return_value=respx.MockResponse(500, text="Server Error")
    )
    config = ClientConfig(base_url="https://api.payelink.example", retries=1)
    async with AsyncAgentSearchClient(api_key="test") as client:
        client._config = config
        from payelink_agent_search.transport import AsyncTransport

        client._transport = AsyncTransport(config)

        with pytest.raises(SdkError):
            await client.search("test")
