from typing import List, TypedDict, Optional

class GovernanceState(TypedDict):
    """
    Represents the state of the API governance validation workflow.

    Attributes:
        old_code: The original code before changes.
        new_code: The new code with modifications.
        changed_code: The specific code snippet that has changed.
        query: The generated query for the vector store based on the code changes.
        relevant_docs: A list of relevant policy documents retrieved from the vector store.
        validation_results: A list of strings, where each string is a validation result
                            (e.g., "Compliant: Rule X" or "Non-compliant: Rule Y").
        report: The final, formatted markdown report of all findings.
        error: An optional string to capture any errors that occur during the process.
    """
    old_code: str
    new_code: str
    changed_code: str
    query: str
    relevant_docs: List[str]
    validation_results: List[str]
    report: str
    error: Optional[str]
