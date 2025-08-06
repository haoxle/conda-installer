import argparse
import yaml
from utils import base_helper
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="Environment Installer",
    description="Installs environments for projects ondemand"
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
        mode = "update" if base_helper.isValidPath(output) else "create"
    else:
        output = Path(conda).parent.parent / env_name
        mode = "update" if base_helper.isValidPath(output) else "create"

    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as tmp:
        yaml.dump(env_dict, tmp)
        temp_yaml_path = tmp.name

    base_helper.installCondaEnv(conda, temp_yaml_path, mode, output)


def main():
    env_file = args.file
    conda = args.conda
    env_dir = args.directory
    output_dir = args.output

    base_helper.isValidFile(conda)

    if env_file is not None and base_helper.isValidFile(env_file):
        with open(env_file, "r") as env:
            env_dict = yaml.safe_load(env)
        install_from_yaml(conda, env_dict, output_dir)

    elif env_dir is not None and base_helper.isValidPath(env_dir):
        for file in Path(env_dir).iterdir():
            if file.is_file() and file.suffix in [".yaml", ".yml"]:
                with open(file, "r") as f:
                    env_dict = yaml.safe_load(f)
                install_from_yaml(conda, env_dict, output_dir)


if __name__ == "__main__":
    main()


#CondaValueError: Environment paths cannot be immediately nested under another conda environment. 
# Check this error to see if it is an issue