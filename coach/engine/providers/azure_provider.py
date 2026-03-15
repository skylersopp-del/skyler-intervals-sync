import os

def call_azure(prompt: str, model: str = None) -> str:
    """
    Plug in your Azure OpenAI / Copilot client here.
    Example (pseudo):

    from openai import AzureOpenAI
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-01",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    resp = client.chat.completions.create(
        model=model or "gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
    """
    raise NotImplementedError("Implement Azure call here.")
