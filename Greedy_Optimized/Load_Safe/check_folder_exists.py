import os

def check_folder_exists(filepath):
    directory = os.path.dirname(filepath)
    
    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        return True
    else:
        return False
