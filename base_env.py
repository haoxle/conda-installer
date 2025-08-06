import argparse
from utils import base_helper
import os

parser = argparse.ArgumentParser(
    prog="Project env installer",
    description="Installs env for the base project.",
)

parser.add_argument("-c", "--miniconda")
parser.add_argument("-o", "--output", default=f"{os.getcwd()}\\env")

args = parser.parse_args()


def main():
    conda = args.miniconda
    output_dir = args.output

    if not base_helper.existsFile(conda):
        raise FileNotFoundError(f"Conda executable not found: {conda}")

    try:
        env_path = os.path.join(os.getcwd(), "env")
        mode = "update" if os.path.isdir(env_path) else "create"
        base_helper.installCondaEnv(conda, f"{env_path}.yml", mode, output_dir)
    except Exception as e:
        raise ValueError(f"Failed to install project env: {e}") from e

if __name__ == "__main__":
    main()