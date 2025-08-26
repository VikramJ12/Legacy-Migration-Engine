import os
from pathlib import Path
from dotenv import load_dotenv

def load_env(env_path: str = None):
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

def ensure_outputs_dir(path='outputs'):
    p = Path(path)
    p.mkdir(exist_ok=True)
    return p

