from langgraph.graph import StateGraph, END

from src.graph.state import GovernanceState
from src.agents.detector import CodeChangeDetectorAgent
from src.agents.validator import ValidatorAgent
from src.agents.reporter import ReporterAgent

def create_governance_graph():
    """
    Creates and configures the LangGraph workflow for API governance.
    """
    # Initialize agents
    detector = CodeChangeDetectorAgent()
    validator = ValidatorAgent()
    reporter = ReporterAgent()

    # Initialize the graph with the state object
    graph = StateGraph(GovernanceState)

    # --- Define Nodes ---
    # Each node is a function or method that the graph will call.
    graph.add_node("detect_changes", detector.find_and_summarize_changes)
    graph.add_node("retrieve_documents", validator.retrieve_documents)
    graph.add_node("validate_code", validator.validate_code)
    graph.add_node("generate_report", reporter.generate_report)

    # --- Define Edges ---
    # This defines the flow of control between the nodes.
    graph.set_entry_point("detect_changes")
    graph.add_edge("detect_changes", "retrieve_documents")
    graph.add_edge("retrieve_documents", "validate_code")
    graph.add_edge("validate_code", "generate_report")
    graph.add_edge("generate_report", END)

    # --- Compile the Graph ---
    # The compiled graph is a runnable object.
    app = graph.compile()
    
    return app

if __name__ == '__main__':
    # This part is for testing the graph compilation
    print("Compiling the governance graph...")
    try:
        app = create_governance_graph()
        print("Graph compiled successfully!")
        # You can also visualize the graph if you have the necessary packages
        # app.get_graph().print_ascii()
    except Exception as e:
        print(f"Error compiling graph: {e}")
