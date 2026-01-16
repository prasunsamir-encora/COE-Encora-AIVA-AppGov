# API Governance Agent

This project is an agentic AI system designed to enforce API governance rules. It uses a multi-agent architecture built with LangGraph to validate API specifications and code against a predefined set of policies.

## Features

- **Policy-driven Validation:** Validates code against governance rules stored in a vector database.
- **Agentic Workflow:** Uses multiple agents (Validator, Reporter) orchestrated by LangGraph.
- **Vectorized Storage:** Chunks and vectorizes governance policies for efficient retrieval using ChromaDB.
- **Extensible:** Easily add new rules and policies by updating the documents in the `data/policies` directory.

## Project Structure

- `data/policies/`: Contains the markdown files for each API governance policy category.
- `src/`: Contains the main source code for the agent system.
  - `agents/`: Holds the logic for individual agents.
  - `graph/`: Defines the LangGraph workflow and state.
  - `utils/`: Provides utility functions for tasks like vector store management.
- `ingest.py`: A script to process policy documents and populate the vector database.
- `main.py`: The main entry point to run the API governance validation.
