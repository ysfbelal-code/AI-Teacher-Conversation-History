import streamlit
from huggingface_hub import InferenceClient

@streamlit.cache_data(show_spinner=False)

def generate_response(prompt: str, temperature: float = 0.3, tokens: int = 512):
    apikey = streamlit.secrets['hf_api']
    models = streamlit.secrets.get('HF_MODELS', [
    "TeichAI/Qwen3-30B-A3B-Thinking-2507-Claude-4.5-Sonnet-High-Reasoning-Distill-GGUF", 
    "TeichAI/Qwen3-4B-Thinking-2507-Claude-Haiku-4.5-High-Reasoning-Distill",
    "TeichAI/Qwen3-4B-Instruct-2507-Claude-Haiku-4.5-Distill",
])
    if not apikey:
        return "Error: hf_api missing in secrets"

    last_err = None
    for m in models:
        try:
            c = InferenceClient(model=m, token=apikey)
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
