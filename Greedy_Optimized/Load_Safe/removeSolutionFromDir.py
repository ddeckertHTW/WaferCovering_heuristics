import os

#Remove the current Probecard Solution json object if it exists. Check if delete is valid is happening before
def removeSolutionFromDir(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        fileName_short = "/".join(filepath.split("/")[-3:])

        print(f"[Removed File] - {fileName_short}")