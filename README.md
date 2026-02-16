# Payelink Agent Search SDK

Discover AI agents across organizations using the **Payelink Agent
Registry Standard**.

The Payelink Agent Search SDK allows applications and agents to discover
other agents that are explicitly published by organizations via a
standardized registry:

    {organization_base_url}/.well-known/agents.json

This SDK is the reference Python implementation of the **Payelink Agent
Discovery Protocol (v0.1)**.

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Architecture](#architecture)
-   [Installation](#installation)
-   [Quick Start](#quick-start)
-   [Async Usage](#async-usage)
-   [Filtering & Options](#filtering--options)
-   [Response Model](#response-model)
-   [Error Handling](#error-handling)
-   [Agent Registry Specification (v0.1)](#agent-registry-specification-v01)
-   [Security Considerations](#security-considerations)
-   [Stability & Versioning](#stability--versioning)
-   [Requirements](#requirements)
-   [License](#license)

------------------------------------------------------------------------

## Overview

AI agents are increasingly hosted by organizations. However, discovering
them in a standardized and structured way remains fragmented.

The Payelink Agent Search SDK solves this by:

-   Fetching organization-published agent registries
-   Parsing agent metadata
-   Returning structured, validated agent results
-   Supporting sync and async usage
-   Enabling filtering

Discovery is **explicit and organization-controlled**. Agents are
discoverable only if their organization lists them in their registry.

------------------------------------------------------------------------

## Architecture

Discovery Flow:

Client Application\
↓\
Payelink Agent Search SDK\
↓\
Fetch `{org}/.well-known/agents.json`\
↓\
Fetch Agent Card(s)\
↓\
Return Structured Agent Results

Key Principles:

-   No internet-wide crawling
-   No scraping
-   Organization opt-in only
-   Registry-based discovery
-   Extensible for identity, payment, and reputation layers

------------------------------------------------------------------------

## Installation

``` bash
pip install payelink-agent-search
```

------------------------------------------------------------------------

## Quick Start

``` python
from payelink_agent_search import AgentSearchClient

client = AgentSearchClient()

response = client.search("Convert USD to KES")

if response.success:
    for agent in response.agents:
        print(f"{agent.agent_name}: {agent.agent_description}")
        print(f"Endpoint: {agent.agent_url}")
else:
    print(f"Error: {response.error}")

client.close()
```

------------------------------------------------------------------------

## Async Usage

``` python
import asyncio
from payelink_agent_search import AsyncAgentSearchClient

async def main():
    async with AsyncAgentSearchClient() as client:
        response = await client.search("translation agent")
        
        if response.success:
            for agent in response.agents:
                print(agent.agent_name)

asyncio.run(main())
```

------------------------------------------------------------------------

## Filtering & Options

``` python
response = client.search(
    query="Financial services",
    allowed_url=[
        "https://org1.example.com",
        "https://org2.example.com"
    ]
)
```

------------------------------------------------------------------------

## Response Model

``` python
class SearchResponse:
    success: bool
    agents: List[AgentDetails]
    error: Optional[str]

class AgentDetails:
    agent_id: Optional[str]
    agent_name: Optional[str]
    agent_description: Optional[str]
    agent_url: Optional[str]
    organization_name: Optional[str]
    organization_url: Optional[str]
```

------------------------------------------------------------------------

## Error Handling

``` python
from payelink_agent_search.errors import SdkError

try:
    response = client.search("test query")
except SdkError as e:
    print(f"SDK Error: {e}")
```

Error Types:

-   `SdkError`
-   `HttpStatusError`
-   `NetworkError`
-   `TimeoutError`
-   `InvalidResponseError`

------------------------------------------------------------------------

## Agent Registry Specification (v0.1)

Organizations must expose:

    GET /.well-known/agents.json

Example:

``` json
{
  "organization": {
    "name": "Acme Finance Ltd",
    "url": "https://acme.com"
  },
  "agents": [
    {
      "id": "budget-planner",
      "card": "https://acme.com/.well-known/agents/budget-planner.json"
    }
  ]
}
```

Each agent card provides extended metadata including:

-   DID-based identity
-   Capabilities
-   Skills
-   Input/output modes
-   Optional pricing metadata

------------------------------------------------------------------------

## Security Considerations

-   Only declared registries are fetched.
-   Organizations control discoverability.
-   Agent cards may include DIDs for identity verification.
-   Future versions may support signed registries.

------------------------------------------------------------------------

## Stability & Versioning

This SDK is currently in **v0.1.x (early development)**. Pre-1.0 releases are not considered stable.

-   The specification may evolve.
-   Breaking changes may occur before v1.0.
-   Schema versions are explicitly declared in registry and agent cards.

------------------------------------------------------------------------

## Requirements

-   Python \>= 3.8
-   httpx \>= 0.24.0
-   pydantic \>= 2.0.0

------------------------------------------------------------------------

## License

MIT License

------------------------------------------------------------------------

Payelink Agent Discovery Protocol • Registry-Based Agent Discovery •
Infrastructure for Interoperable AI Agents
