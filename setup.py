from pathlib import Path

base_directory = Path.home() / "Chatty"

#checks if this is the first time running the app/ The required folders exist
def initialize_directories():
    if not base_directory.exists():
        base_directory.mkdir(parents=True)
        for folder in ["Messages", "Friends", "Config"]:
            (base_directory / folder).mkdir(parents=True, exist_ok=True)

