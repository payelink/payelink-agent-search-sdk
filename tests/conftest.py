"""Pytest fixtures and configuration."""
import pytest

from payelink_agent_search.config import ClientConfig


@pytest.fixture
def client_config():
    """Default config for tests (base_url used by respx mocks)."""
    return ClientConfig(base_url="https://api.payelink.example", retries=1)


@pytest.fixture
def sample_search_response():
    """Valid API search response payload."""
    return {
        "success": True,
        "message": "Found 2 agent(s)",
        "data": [
            {
                "agent_id": "agent-1",
                "agent_name": "Currency Converter",
                "agent_description": "Converts between currencies",
                "agent_url": "https://example.com/agents/currency",
                "organization_name": "Acme Inc",
                "organization_url": "https://example.com",
            },
            {
                "agent_id": "agent-2",
                "agent_name": "Budget Planner",
                "agent_description": "Helps plan budgets",
                "agent_url": "https://example.com/agents/budget",
                "organization_name": "Acme Inc",
                "organization_url": "https://example.com",
            },
        ],
    }
