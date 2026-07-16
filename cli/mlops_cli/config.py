import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".mlops"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"server_url": "", "access_token": None, "refresh_token": None}

def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
