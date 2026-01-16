import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.llm.model import create_llm
from src.graph.state import GovernanceState
from src.utils.vector_store import get_retriever

load_dotenv()

class ValidatorAgent:
    """
    An agent that validates code changes against API governance policies.
    """

    def __init__(self):
        # api_key = os.getenv("OPENAI_API_KEY")
        # if not api_key:
        #     raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        # Using a more advanced model for better reasoning
        self.llm = create_llm() #ChatOpenAI(api_key=api_key, model="gpt-5", temperature=0)

        self.retriever = get_retriever(k_results=5)



    def _create_validation_chain(self):
        """Creates a chain to validate code against a specific rule."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an API governance expert. Your task is to validate a code snippet against a specific governance rule. Be precise and clear in your judgment."),
            ("user", "Does the following code comply with this rule?\n\nRule: {rule}\n\nCode:\n```\n{code}\n```\n\nRespond with 'Compliant' or 'Non-compliant', followed by a brief, one-sentence explanation.")
        ])
        return prompt | self.llm | StrOutputParser()

    def generate_query(self, state: GovernanceState) -> GovernanceState:
        """Generates a search query based on the changed code."""
        print("---AGENT: Generating search query---")
        code = state["changed_code"]
        if not code:
            return {**state, "error": "No code provided for validation."}
            
        query_generation_chain = self._create_query_generation_chain()
        query = query_generation_chain.invoke({"code": code})
        
        print(f"Generated Query: {query}")
        return {**state, "query": query}

    def retrieve_documents(self, state: GovernanceState) -> GovernanceState:
        """Retrieves relevant documents from the vector store."""
        print("---AGENT: Retrieving relevant documents---")
        query = state["query"]
        if not query or query == "No changes detected.":
            print("No changes detected or query is empty. Skipping document retrieval.")
            return {**state, "relevant_docs": []}
            
        retrieved_docs = self.retriever.invoke(query)
        print(f"Found {len(retrieved_docs)} documents.")
        
        # Storing just the page content for simplicity
        doc_contents = [doc.page_content for doc in retrieved_docs]
        return {**state, "relevant_docs": doc_contents}

    def validate_code(self, state: GovernanceState) -> GovernanceState:
        """Validates the code against each retrieved document."""
        print("---AGENT: Validating code against documents---")
        code = state["changed_code"]
        docs = state["relevant_docs"]
        
        if not docs:
            return {**state, "validation_results": ["No relevant governance documents found to validate against."]}

        validation_chain = self._create_validation_chain()
        results = []
        
        for doc in docs:
            result = validation_chain.invoke({"rule": doc, "code": code})
            results.append(result)
            print(f"  - Validation Result: {result}")
            
        return {**state, "validation_results": results}
