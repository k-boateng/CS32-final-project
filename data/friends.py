import json
from pathlib import Path

FRIENDS_DIR = Path.home() / "messageapp" / "Friends"
FRIENDS_DIR.mkdir(parents=True, exist_ok=True)

def add_friend(name, ip, port):
    friend_file = FRIENDS_DIR / f"{name}.json"
    with open(friend_file, 'w') as f:
        json.dump({"ip": ip, "port": port}, f)

def get_friends():
    friends = []
    for file in FRIENDS_DIR.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            friends.append((file.stem, data['ip'], data['port']))
    return friends

def get_friend_details(name):
    file = FRIENDS_DIR / f"{name}.json"
    if file.exists():
        with open(file) as f:
            return json.load(f)
    return None
