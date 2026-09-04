from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

root_dir = Path(__file__).resolve().parent.parent.parent
LLM_API_KEY = os.getenv("OPEN_AI")
DEFAULT_LLM = "gpt-4.1-nano"
