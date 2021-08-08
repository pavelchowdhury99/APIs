import yaml

def read_yaml(filepath):
    """
    Reads YAML file and return a dictionary
    """
    with open(filepath) as f:
        return yaml.safe_load(f)
