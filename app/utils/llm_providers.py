from abc import ABC, abstractmethod
from openai import OpenAI
from typing import Dict, Any

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str = None, **kwargs):
        """Initialize the LLM provider with configuration"""
        self.client = OpenAI(
            base_url=self.BASE_URL,
            api_key=api_key
        )
        self.model = kwargs.get('model', self.DEFAULT_MODEL)
        self.temperature = kwargs.get('temperature', 0.0)
    
    def call(self, instruction: str, prompt: str, **kwargs) -> str:
        """Call the LLM with the given instruction and prompt"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content

class OllamaProvider(LLMProvider):
    """Provider for Ollama LLM service"""
    BASE_URL = 'http://localhost:11434/v1'
    DEFAULT_MODEL = 'llama3.1:latest'
    
    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(
            api_key=api_key or 'ollama',  # required but unused
            **kwargs
        )

class GroqProvider(LLMProvider):
    """Provider for Groq LLM service"""
    BASE_URL = "https://api.groq.com/openai/v1"
    DEFAULT_MODEL = 'llama-3.3-70b-versatile'
    
    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(
            api_key=api_key,
            **kwargs
        )

class GeminiProvider(LLMProvider):
    """Provider for Google Gemini LLM service"""
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    DEFAULT_MODEL = 'gemini-2.0-flash'
    
    def __init__(self, api_key: str = None, **kwargs):
        super().__init__(
            api_key=api_key,
            **kwargs
        )

# Provider factory
def get_provider(provider_name: str, **kwargs) -> LLMProvider:
    """Factory function to get the appropriate LLM provider"""
    providers = {
        'ollama': OllamaProvider,
        'groq': GroqProvider,
        'gemini': GeminiProvider
    }
    
    if provider_name.lower() not in providers:
        raise ValueError(f"Unknown provider: {provider_name}. Available providers: {', '.join(providers.keys())}")
    
    return providers[provider_name.lower()](**kwargs) 