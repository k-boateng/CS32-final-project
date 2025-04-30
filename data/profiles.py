import os
from pathlib import Path

CONFIG_DIR = Path.home() / "messageapp" / "Config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_PATH = CONFIG_DIR / "profile.txt"

def save_username(name):
    with open(PROFILE_PATH, 'w') as f:
        f.write(name)

def get_username():
    if PROFILE_PATH.exists():
        return PROFILE_PATH.read_text().strip()
    return "User"
