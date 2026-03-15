import os

def call_openai(prompt: str, model: str = None) -> str:
    """
    Plug in your OpenAI client here.
    Example (pseudo):

    import openai
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=model or "gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
    """
    raise NotImplementedError("Implement OpenAI call here.")
