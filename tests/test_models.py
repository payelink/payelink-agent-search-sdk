"""Tests for Pydantic models (SearchRequest, AgentDetails, SearchResponse)."""
import pytest
from pydantic import ValidationError

from payelink_agent_search.models import (
    AgentDetails,
    SearchRequest,
    SearchResponse,
)


def test_search_request_minimal():
    """SearchRequest accepts only required query."""
    req = SearchRequest(query="Convert USD to KES")
    assert req.query == "Convert USD to KES"
    assert req.max_result == 10
    assert req.country is None
    assert req.allowed_url is None


def test_search_request_with_filters():
    """SearchRequest accepts all optional filters."""
    req = SearchRequest(
        query="finance",
        max_result=5,
        country="KE",
        capability="streaming",
        default_input_mode=["text/plain"],
        default_output_mode=["application/json"],
        allowed_url=["https://org.example.com"],
    )
    assert req.max_result == 5
    assert req.country == "KE"
    assert req.capability == "streaming"
    assert req.default_input_mode == ["text/plain"]
    assert req.allowed_url == ["https://org.example.com"]


def test_search_request_query_required():
    """SearchRequest requires query."""
    with pytest.raises(ValidationError):
        SearchRequest()


def test_agent_details_from_dict():
    """AgentDetails can be built from API-like dict."""
    data = {
        "agent_id": "budget-planner",
        "agent_name": "Budget Planner",
        "agent_description": "Helps plan budgets",
        "agent_url": "https://acme.com/.well-known/agents/budget-planner.json",
        "organization_name": "Acme Finance Ltd",
        "organization_url": "https://acme.com",
    }
    agent = AgentDetails(**data)
    assert agent.agent_id == "budget-planner"
    assert agent.agent_name == "Budget Planner"
    assert agent.organization_url == "https://acme.com"


def test_agent_details_optional_fields():
    """AgentDetails allows None for all fields (API may omit)."""
    agent = AgentDetails()
    assert agent.agent_id is None
    assert agent.agent_name is None


def test_search_response_success():
    """SearchResponse with success and agents."""
    resp = SearchResponse(
        success=True,
        agents=[
            AgentDetails(agent_id="1", agent_name="Agent One"),
            AgentDetails(agent_id="2", agent_name="Agent Two"),
        ],
        message="Found 2 agent(s)",
    )
    assert resp.success is True
    assert len(resp.agents) == 2
    assert resp.error is None


def test_search_response_failure():
    """SearchResponse with success=False and error message."""
    resp = SearchResponse(success=False, agents=[], error="API error")
    assert resp.success is False
    assert resp.agents == []
    assert resp.error == "API error"
