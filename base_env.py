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
    base_helper.isValidFile(conda)

    try:
        if os.path.isdir(f"{os.getcwd()}\\env"):
            base_helper.installCondaEnv(conda, f"{os.getcwd()}\\env.yml", "update", output_dir)
        else:
            base_helper.installCondaEnv(conda, f"{os.getcwd()}\\env.yml", "create", output_dir)
    except:
        raise ValueError("Failed to install project env")


if __name__ == "__main__":
    main()