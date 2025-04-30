from pathlib import Path

CONFIG_DIR = Path.home() / "messageapp/Config"
PROFILE_FILE = CONFIG_DIR / "username.txt"

def get_username():
    if PROFILE_FILE.exists():
        return PROFILE_FILE.read_text().strip()
    return None

def set_username(name):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_FILE.write_text(name.strip())
