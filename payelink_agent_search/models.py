from typing import List, Literal, Optional

from pydantic import BaseModel, Field

InputMode = Literal[
    "text/plain",
    "application/json",
    "text/markdown",
]

OutputMode = Literal[
    "text/plain",
    "application/json",
    "text/markdown",
]

class SearchRequest(BaseModel):
    query: str = Field(..., description="The query to search for")
    max_result: Optional[int] = Field(
        10, description="The max number of agents to return"
    )
    country: Optional[str] = Field(None, description="The country of the agent")
    capability: Optional[Literal['streaming', 'pushNotifications']] = Field(None, description="The capability the agent should support")
    default_input_mode: Optional[List[InputMode]] = Field(None, description="The default input mode the agent should support")
    default_output_mode: Optional[List[OutputMode]] = Field(None, description="The default output mode the agent should support")
    search_depth: Optional[Literal["advanced", "basic"]] = Field(None, description="Controls the latency vs. relevance tradeoff ")
    allowed_url: Optional[List[str]] = Field(
        None,
        description="If set, these URLs are used as the discovered organizations.",
    )


class AgentDetails(BaseModel):
    agent_id: Optional[str] = Field(None, description="The unique identifier of the agent")
    agent_name: Optional[str] = Field(None, description="The name of the agent")
    agent_description: Optional[str] = Field(None, description="The description of the agent")
    agent_url: Optional[str] = Field(None, description="The URL of the agent's card")
    organization_name: Optional[str] = Field(None, description="The name of the organization")
    organization_url: Optional[str] = Field(None, description="The URL of the organization")

class SearchResponse(BaseModel):
    success: bool = Field(..., description="Whether the request succeeded")
    agents: List[AgentDetails] = Field(default_factory=list)
    message: Optional[str] = Field(None, description="Optional message from the API (e.g. 'Found N agent(s)')")
    error: Optional[str] = None

