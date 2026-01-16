import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.llm.model import create_llm

from src.graph.state import GovernanceState

load_dotenv()

class CodeChangeDetectorAgent:
    """
    An agent that detects changes between two versions of code and summarizes them.
    """

    def __init__(self):
        # api_key = os.getenv("OPENAI_API_KEY")
        # if not api_key:
        #     raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.llm = create_llm() #ChatOpenAI(api_key=api_key, model="gpt-5", temperature=0)

    def _create_change_detection_chain(self):
        """Creates a chain to identify and summarize code changes."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a code analysis expert. Your task is to compare two versions of a Python file and identify the key changes related to API endpoints. "
                "You must respond in a specific JSON format."
            )),
            ("user", (
                "Below are two versions of a Python file. Please analyze the changes from the old code to the new code.\n\n"
                "## Old Code:\n"
                "```python\n{old_code}\n```\n\n"
                "## New Code:\n"
                "```python\n{new_code}\n```\n\n"
                "Now, perform these two tasks:\n"
                "1.  Extract the full code of the **new or modified** API endpoint, function, or class from the 'New Code'.\n"
                "2.  Write a concise, one-sentence summary of the change (e.g., 'A new endpoint /user-details/getUser was added' or 'The authentication method for /orders was updated').\n\n"
                "Respond with a single JSON object containing two keys: `changed_code_snippet` and `change_summary`."
            ))
        ])
        return prompt | self.llm | StrOutputParser()

    def find_and_summarize_changes(self, state: GovernanceState) -> GovernanceState:
        """Analyzes code versions and updates the state with the findings."""
        print("---AGENT: Detecting code changes---")
        old_code = state["old_code"]
        new_code = state["new_code"]

        if old_code == new_code:
            return {**state, "changed_code": "", "query": "No changes detected."}

        change_detection_chain = self._create_change_detection_chain()
        llm_response = change_detection_chain.invoke({"old_code": old_code, "new_code": new_code})

        try:
            # The response might be in a markdown code block, so we clean it up
            cleaned_response = llm_response.strip().replace("```json", "").replace("```", "")
            response_json = json.loads(cleaned_response)
            
            changed_code = response_json.get("changed_code_snippet", "")
            summary = response_json.get("change_summary", "No summary provided.")

            print(f"Detected Change: {summary}")
            print(f"Changed Snippet:\n{changed_code}")

            return {**state, "changed_code": changed_code, "query": summary}
        except json.JSONDecodeError:
            error_message = "Failed to parse change detection response from LLM."
            print(f"ERROR: {error_message}")
            print(f"LLM Response was: {llm_response}")
            return {**state, "error": error_message}
