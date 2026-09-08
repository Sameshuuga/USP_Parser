from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

root_dir = Path(__file__).resolve().parent.parent.parent
data_dir = root_dir / "data/"
log_file = data_dir / "main.log"
default_input_dir = data_dir / "input"


LLM_API_KEY = os.getenv("OPEN_AI")
DEFAULT_LLM = "gpt-4.1-nano"
