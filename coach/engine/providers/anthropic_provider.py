import os

def call_anthropic(prompt: str, model: str = None) -> str:
    """
    Plug in your Anthropic client here.
    Example (pseudo):

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=model or "claude-3-5-sonnet-20240620",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text
    """
    raise NotImplementedError("Implement Anthropic call here.")
