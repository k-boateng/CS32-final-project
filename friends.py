from pathlib import Path
import json

FRIENDS_DIR = Path.home() / "messageapp/Friends"

FRIENDS_DIR.mkdir(parents=True, exist_ok=True)

def add_friend(ip, port, name):
    data = {"ip": ip, "port": port, "name": name}
    friend_file = FRIENDS_DIR / f"{name}.json"
    with open(friend_file, 'w') as f:
        json.dump(data, f)

def get_friends():
    friends = []
    for file in FRIENDS_DIR.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            friends.append(data)
    return friends

def friend_exists(name):
    return (FRIENDS_DIR / f"{name}.json").exists()