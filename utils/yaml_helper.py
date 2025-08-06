import yaml

def validateCondaYaml(yaml_file):
    # Can probably expand this to raise a specific error, if they key is not one of these then raise the error
    
    valid_keys = ["name", "channels", "output", "dependencies"]
    
    with open(yaml_file, "r") as env:
        env_dict = yaml.safe_load(env)

        for key in env_dict:
            if key not in valid_keys:
                raise yaml.YAMLError(f"{yaml_file}: not a valid conda yaml, {key} is not a valid configuration.")
    return True