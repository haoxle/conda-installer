import os
from pathlib import Path
import subprocess


def getEnvList(directory: str) -> list[Path]:
    """
    Returns a list of files in the given directory.

    Args:
        directory (str): Relative or absolute path to a directory.

    Returns:
        List[Path]: List of Path objects representing files in the directory.
    """
    env_dir = Path(__file__).parent / directory
    env_list = [f for f in env_dir.iterdir() if f.is_file()]
    return env_list


def existsDir(dirPath: str) -> bool:
    """
    Checks if a given directory path exists.

    Args:
        dirPath (str): The path to the directory.

    Returns:
        bool: True if directory exists, False otherwise.
    """
    return os.path.isdir(dirPath)


def existsFile(filePath: str) -> bool:
    """
    Checks if a given file path exists.

    Args:
        filePath (str): The path to the file.

    Returns:
        bool: True if file exists, False otherwise.
    """
    return os.path.isfile(filePath)


def isYaml(filePath: str):
    """
    Validates if the given file has a YAML extension.

    Args:
        filePath (str): Path to the file.

    Raises:
        ValueError: If the file extension is not .yaml or .yml.
    """
    if Path(filePath).suffix.lower() in ['.yaml', '.yml']:
        print("File seems to be YAML")
    else:
        raise ValueError("File does not appear to be a YAML file.")


def installCondaEnv(conda: str, env_file_path: str, action: str, output_path: Path | None = None):
    """
    Runs conda env create/update command with the given parameters.

    Args:
        conda (str): Path to conda executable.
        env_file_path (str): Path to the environment YAML file.
        action (str): Either "create" or "update".
        output_path (Path | None): Path where environment should be created/updated.

    Raises:
        subprocess.CalledProcessError: If the conda command fails.
    """
    try:
        print(f"{action} conda environment using: {output_path}")
        cmd_arr = [conda, "env", action, "-f", str(env_file_path)]
        if output_path:
            cmd_arr.extend(["-p", str(output_path)])

        # Run the command and capture output for better error reporting
        completed = subprocess.run(cmd_arr, check=True, capture_output=True, text=True)
        print(completed.stdout)

    except subprocess.CalledProcessError as e:
        # stderr can be None, fallback to e.output or str(e)
        error_msg = e.stderr or e.output or str(e)
        print(f"An error occurred while updating the Conda environment:\n{error_msg}")
        raise