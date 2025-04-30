from dotenv import load_dotenv
import os
from app.utils.llm_providers import get_provider

load_dotenv()

def call_llm(instruction, prompt, provider_name="ollama", **kwargs):
    """
    Call the specified LLM provider with the given instruction and prompt.
    
    Args:
        instruction (str): The system instruction for the LLM
        prompt (str): The user prompt for the LLM
        provider_name (str): Name of the LLM provider to use (default: "ollama")
        **kwargs: Additional arguments to pass to the provider
        
    Returns:
        str: The LLM's response
    """
    # Get provider-specific configuration from environment variables
    provider_config = {
        'api_key': os.getenv(f"{provider_name.upper()}_API_KEY"),
        **kwargs
    }
    
    # Get the appropriate provider
    provider = get_provider(provider_name, **provider_config)
    
    # Call the provider
    return provider.call(instruction, prompt)