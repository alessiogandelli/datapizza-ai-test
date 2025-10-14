from dotenv import load_dotenv
import os
from datapizza.clients.openai import OpenAIClient

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
)

# Optionally export what other modules need
__all__ = ['client']