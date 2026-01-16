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
    
    documentation_modes: List[Literal["technical", "functional"]] = field(
        default_factory=lambda: ["technical", "functional"]
    )

    extracted_code: Optional[Dict[str, Any]] = None

    # This is only for the flow based documentation information required
    call_tree: Optional[str]
    methods_code: Optional[str]

    prompts: Dict[str, str] = field(default_factory=dict)

    documentation_results: Dict[str, str] = field(default_factory=dict)