import os
from pathlib import Path

#Organization

#If new user, this folder will not exist.
base_directory = Path.home() / "messageapp"

def is_new_user():

     #Checks if this folder exists
    if not base_directory.exists(): #Create a new folder
        base_directory.mkdir(parents=True)

        new_folders = ["Messages", "Friends", "Config"]

        for folder in new_folders:
            folder_path = base_directory / folder  # Append the folder name to the base directory
            folder_path.mkdir(parents=True, exist_ok=True)
    return None

def starting_page():

    contents = os.listdir(base_directory/"Friends")

    if not contents:
        print("No messages yet")

