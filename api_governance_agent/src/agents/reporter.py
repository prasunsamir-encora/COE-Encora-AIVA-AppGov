import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.llm.model import create_llm
from src.graph.state import GovernanceState

load_dotenv()

class ReporterAgent:
    """
    An agent that compiles validation results into a final report.
    """

    def __init__(self):
        # api_key = os.getenv("OPENAI_API_KEY")
        # if not api_key:
        #     raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.llm = create_llm() #ChatOpenAI(api_key=api_key, model="gpt-5", temperature=0)

    def _create_reporting_chain(self):
        """Creates a chain to generate a formatted report from validation results."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in API governance reporting. Your task is to create a clear, concise, and actionable summary report from a list of validation findings."),
            ("user", (
                "Please generate a markdown report based on the following validation results for the provided code snippet.\n\n"
                "## Code Under Review:\n"
                "```\n{code}\n```\n\n"
                "## Validation Findings:\n"
                "{findings}\n\n"
                "Structure the report with two main sections: '## Compliant Checks' and '## Non-compliant Issues'. "
                "If there are non-compliant issues, provide a '### Recommendations' section with suggested fixes."
            ))
        ])
        return prompt | self.llm | StrOutputParser()

    def generate_report(self, state: GovernanceState) -> GovernanceState:
        """Generates a final report from the validation results."""
        print("---AGENT: Generating final report---")
        code = state["changed_code"]
        results = state["validation_results"]

        if not results:
            return {**state, "report": "No validation was performed."}

        findings_str = "\n".join(f"- {res}" for res in results)
        
        reporting_chain = self._create_reporting_chain()
        report = reporting_chain.invoke({"code": code, "findings": findings_str})
        
        print("---REPORT---")
        print(report)
        
        return {**state, "report": report}
