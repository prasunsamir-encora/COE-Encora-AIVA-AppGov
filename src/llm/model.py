import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

def create_llm() -> AzureChatOpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment.")

    endpoint = os.environ.get("API_AZURE_ENDPOINT")
    if not endpoint:
        raise RuntimeError("API_AZURE_ENDPOINT is not set in environment.")
    
    deployment = os.environ.get("API_AZURE_MODEL_DEPLOYMENT")
    if not deployment:
        raise RuntimeError("API_AZURE_MODEL_DEPLOYMENT is not set in environment.")

    api_version = os.environ.get("API_ENDPOINT_VERSION")
    if not api_version:
        raise RuntimeError("API_ENDPOINT_VERSION is not set in environment.")


    return AzureChatOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        azure_deployment=deployment,
        api_version=api_version,
        temperature=1
    )