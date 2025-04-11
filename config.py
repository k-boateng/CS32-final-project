from pathlib import Path


#If new user, this folder will not exist.

def is_new_user():
    
    folder_path = Path.home() / "messageapp" #Checks if this folder exists
    
    if not folder_path.exists(): #Create a new folder
        folder_path.mkdir(parents=True)

    return None

