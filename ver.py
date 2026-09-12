import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(".").resolve() / ".env")
print(repr(os.getenv("GROQ_API_KEY")))