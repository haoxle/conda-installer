import yaml
from pathlib import Path
import tempfile
from typing import Optional
from . import base_helper

def validateCondaYaml(yaml_file: str) -> bool:
    """
    Validates that the YAML file contains only allowed top-level keys for a Conda environment file.
    Also checks that required keys ('name' and 'dependencies') exist and the file is not empty.

    Args:
        yaml_file (str): Path to the YAML file.

    Raises:
        yaml.YAMLError: If the file is empty, missing required keys, or contains invalid keys.

    Returns:
        bool: True if validation passes.
    """
    
    valid_keys = ["name", "channels", "output", "dependencies"]

    with open(yaml_file, "r") as env:
        env_dict = yaml.safe_load(env)

    if not env_dict:
        raise yaml.YAMLError(f"{yaml_file}: YAML file is empty.")

    missing_keys = [key for key in ["name", "dependencies"] if key not in env_dict]
    if missing_keys:
        raise yaml.YAMLError(f"{yaml_file}: Missing required key(s): {', '.join(missing_keys)}")

    for key in env_dict:
        if key not in valid_keys:
            raise yaml.YAMLError(
                f"{yaml_file}: not a valid conda YAML. '{key}' is not a valid configuration key."
            )
    return True


def is_existing_conda_env(path: Path) -> bool:
    """
    Checks whether a given path is an existing Conda environment by verifying
    that the path exists and contains the 'conda-meta' directory.

    Args:
        path (Path): Path to check.

    Returns:
        bool: True if the path is a Conda environment, False otherwise.
    """
    
    return path.is_dir() and (path / "conda-meta").is_dir()


def install_from_yaml(conda: str, env_dict: dict, output_dir: Optional[str] = None) -> None:
    """
    Convenience function to load an environment YAML file, validate it,
    and install/update the environment.

    Args:
        conda (str): Path to the conda executable.
        env_dict (dict): Parsed YAML environment dictionary.
        output_dir (Optional[str]): Base directory for environment installation.

    Raises:
        yaml.YAMLError: If YAML validation fails.
        Exception: If installation fails.
    """
    
    env_name = env_dict.get("name")
    output_base = env_dict.pop("output", None) or output_dir

    if output_base:
        output = Path(output_base) / env_name
    else:
        output = Path(conda).parent.parent / "envs" / env_name

    mode = "update" if is_existing_conda_env(output) else "create"

    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as tmp:
        yaml.dump(env_dict, tmp)
        temp_yaml_path = tmp.name

    output.parent.mkdir(parents=True, exist_ok=True)

    base_helper.installCondaEnv(conda, temp_yaml_path, mode, output)
