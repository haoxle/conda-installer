import argparse
import yaml
from pathlib import Path
import tempfile
import sys
from utils import base_helper
from utils.yaml_helper import validateCondaYaml

parser = argparse.ArgumentParser(
    prog="Environment Installer",
    description="Installs environments for projects on demand"
)

parser.add_argument("-c", "--conda")
parser.add_argument("-d", "--directory", default=None)
parser.add_argument("-f", "--file", default=None)
parser.add_argument("-o", "--output", default=None)

args = parser.parse_args()


def install_from_yaml(conda, env_dict, output_dir=None):
    env_name = env_dict.get("name")
    output_base = env_dict.pop("output", None) or output_dir

    if output_base:
        output = Path(output_base) / env_name
        mode = "update" if base_helper.existsFile(output) else "create"
    else:
        output = Path(conda).parent.parent / "envs" / env_name
        mode = "update" if base_helper.existsDir(output) else "create"

    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as tmp:
        yaml.dump(env_dict, tmp)
        temp_yaml_path = tmp.name

    output.parent.mkdir(parents=True, exist_ok=True)

    base_helper.installCondaEnv(conda, temp_yaml_path, mode, output)


def main():
    env_file = args.file
    conda = args.conda
    env_dir = args.directory
    output_dir = args.output

    if not base_helper.existsFile(conda):
        raise FileNotFoundError(f"Conda executable not found: {conda}")

    failures = 0

    if env_file and base_helper.existsFile(env_file):
        try:
            validateCondaYaml(env_file)
            with open(env_file, "r") as env:
                env_dict = yaml.safe_load(env)
            install_from_yaml(conda, env_dict, output_dir)
        except Exception as e:
            print(f"Failed to install environment from file {env_file}: {e}")
            failures += 1

    elif env_dir and base_helper.existsDir(env_dir):
        for file in Path(env_dir).iterdir():
            if file.is_file() and file.suffix in [".yaml", ".yml"]:
                try:
                    validateCondaYaml(file)
                    with open(file, "r") as f:
                        env_dict = yaml.safe_load(f)
                    install_from_yaml(conda, env_dict, output_dir)
                except Exception as e:
                    print(f"Failed to install environment from file {file}: {e}")
                    failures += 1
    
    if failures > 0:
        print(f"\n {failures} environment(s) failed to install.")
        sys.exit(1)

    print("\nAll environments installed successfully.")

if __name__ == "__main__":
    main()