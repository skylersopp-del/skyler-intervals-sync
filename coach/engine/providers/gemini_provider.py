import os

def call_gemini(prompt: str, model: str = None) -> str:
    """
    Plug in your Gemini client here.
    Example (pseudo):

    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    m = genai.GenerativeModel(model or "gemini-1.5-flash")
    resp = m.generate_content(prompt)
    return resp.text
    """
    raise NotImplementedError("Implement Gemini call here.")
