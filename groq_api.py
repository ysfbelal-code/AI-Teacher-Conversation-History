import streamlit
from openai import OpenAI

@streamlit.cache_data(show_spinner=False)

def generate_response(prompt: str, temperature: float = 0.3, tokens: int = 512):
    url = "https://api.groq.com/openai/v1"
    apikey = streamlit.secrets['groq_api']
    models = streamlit.secrets.get('GROQ_MODELS', ['qwen/qwen3-32b', 'moonshotai/kimi-k2-instruct', 'llama-3.3-70b-versatile',])
    if not apikey:
        return "Error: hf_api missing in secrets"

    last_err = None
    for m in models:
        try:
            c = OpenAI(api_key=apikey, base_url=url)
            r = c.chat.completions.create(
                model=m,
                messages=[{'role': 'user', 'content': prompt}],
                temperature=temperature,
                max_tokens=tokens
            )
            content = r.choices[0].message.content
            if content is not None:
                return content
        except Exception as e:
            last_err = e

    if last_err is None:
        return "Error: no models available"

    return (
        "HF model failed."
        f"Tried models: {models}"
        "Fix:"
        "1) Switch to Groq by inserting Groq's models and changing to your Groq API key, or"
        "2) Replace HF model in MODELS.\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )
