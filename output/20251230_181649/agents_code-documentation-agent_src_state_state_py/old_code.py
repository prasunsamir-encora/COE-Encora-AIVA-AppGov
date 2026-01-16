from typing import TypedDict, Annotated, Literal, List, Dict, Optional, Any
from langgraph.graph.message import add_messages
from dataclasses import dataclass, field


# Here we can use MessageGraph to improve on the AgentState

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_documentation_type: str
    path_file: str
    next_node: str
    class_fqn: str
    needs_chuncking: bool
    retries: int
    error_message: Optional[str]
    
    documentation_modes: List[Literal["technical", "functional"]] = field(
        default_factory=lambda: ["technical", "functional"]
    )

    extracted_code: Optional[Dict[str, Any]] = None

    prompts: Dict[str, str] = field(default_factory=dict)

    documentation_results: Dict[str, str] = field(default_factory=dict)

    # These fields are only required for the flow based documentation information 
    call_tree: Optional[str]
    methods_code: Optional[str]
    cypher_query: Optional[str]