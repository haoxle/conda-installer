import yaml

def validateCondaYaml(yaml_file):
    """
    Validates that the YAML file contains only allowed top-level keys
    for a Conda environment file.
    """
    valid_keys = ["name", "channels", "output", "dependencies"]

    with open(yaml_file, "r") as env:
        env_dict = yaml.safe_load(env)

        for key in env_dict:
            if key not in valid_keys:
                raise yaml.YAMLError(
                    f"{yaml_file}: not a valid conda YAML. '{key}' is not a valid configuration key."
                )
    return True