import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "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")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
