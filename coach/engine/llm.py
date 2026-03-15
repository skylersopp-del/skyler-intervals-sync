from typing import Literal
from .providers.openai_provider import call_openai
from .providers.anthropic_provider import call_anthropic
from .providers.gemini_provider import call_gemini
from .providers.azure_provider import call_azure

Provider = Literal["openai", "anthropic", "gemini", "azure"]

def call_model(prompt: str, provider: Provider, model: str | None = None) -> str:
    if provider == "openai":
        return call_openai(prompt, model=model)
    if provider == "anthropic":
        return call_anthropic(prompt, model=model)
    if provider == "gemini":
        return call_gemini(prompt, model=model)
    if provider == "azure":
        return call_azure(prompt, model=model)
    raise ValueError(f"Unknown provider: {provider}")
