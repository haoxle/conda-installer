import argparse
import yaml
from pathlib import Path
import sys
from utils import base_helper
from utils.yaml_helper import validateCondaYaml, install_from_yaml
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.log_helper import info, error, success

parser = argparse.ArgumentParser(
    prog="Environment Installer",
    description="Installs environments for projects on demand"
)

parser.add_argument("-c", "--conda")
parser.add_argument("-d", "--directory", default=None)
parser.add_argument("-f", "--file", default=None)
parser.add_argument("-o", "--output", default=None)

args = parser.parse_args()

def process_env_file(conda, file_path, output_dir, progress, failures):
    try:
        validateCondaYaml(file_path)
        with open(file_path, "r") as env:
            env_dict = yaml.safe_load(env)
        env_name = env_dict.get("name", "env")
        task = progress.add_task(f"[cyan]Installing {env_dict.get('name', 'env')}...", total=1)
        install_from_yaml(conda, env_dict, output_dir)
        progress.update(task, description=f"[green]Installed {env_dict.get('name', 'env')}")
        success(f"{env_name} installed successfully.")
    except Exception as e:
        error(f"Failed to install environment from file {file_path}: {e}")
        failures.append(file_path)

def main():
    env_file = args.file
    conda = args.conda
    env_dir = args.directory
    output_dir = args.output

    if not base_helper.existsFile(conda):
        raise FileNotFoundError(f"Conda executable not found: {conda}")

    failures = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        if env_file and base_helper.existsFile(env_file):
            process_env_file(conda, env_file, output_dir, progress, failures)
        elif env_dir and base_helper.existsDir(env_dir):
            for file in Path(env_dir).iterdir():
                if file.is_file() and file.suffix in [".yaml", ".yml"]:
                    process_env_file(conda, file, output_dir, progress, failures)

        else:
            error("No valid file or directory input provided.")
            sys.exit(1)
                    
    if failures:
        error(f"{len(failures)} environment(s) failed to install:")
        for f in failures:
            error(f"- {f}")
        sys.exit(1)

    success("All environments installed successfully.")


if __name__ == "__main__":
    main()