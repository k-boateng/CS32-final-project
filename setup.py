from pathlib import Path

base_directory = Path.home() / "messageapp"

def initialize_directories():
    if not base_directory.exists():
        base_directory.mkdir(parents=True)
        for folder in ["Messages", "Friends", "Config"]:
            (base_directory / folder).mkdir(parents=True, exist_ok=True)

def get_base_directory():
    return base_directory
