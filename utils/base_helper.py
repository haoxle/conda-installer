from pathlib import Path


def getEnvList(directory):
    env_dir = Path(__file__).parent / directory
    env_list = [f for f in env_dir.iterdir() if f.is_file()]
    return env_list

# Does this also check for files?
def isValidPath(dirPath):
    """
    Checks if a given directory path exists.

    Args:
        dirPath (str): The path to the directory.

    Raises:
        ValueError: If the path does not exist.
    """

    import os

    if not os.path.isdir(dirPath):
        return False
    return True


def isValidFile(filePath):
    """
    Checks if a given file path exists.

    Args:
        dirPath (str): The path to the file.

    Raises:
        ValueError: If the file does not exist.
    """

    import os

    if not os.path.isfile(filePath):
        return False
    return True


def isYaml(dirPath):
    if Path(dirPath).suffix in ['.yaml', '.yml']:
        print("File seems to be YAML")
    else:
        raise ValueError("File does not appear to be a YAML file.")
    

def installCondaEnv(conda, dirPath, action, outputPath=None):
    import subprocess
    from pathlib import Path

    try:
        print(f"{action} conda using: {outputPath}")
        cmd_arr = [conda, "env", action, "-f", str(dirPath)]
        if outputPath:
            cmd_arr.extend(["-p", str(Path(outputPath))]) 
        subprocess.run(args=cmd_arr, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while updating the Conda environment: {e.stderr}")
