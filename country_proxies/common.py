import yaml

def read_yaml(file_path):
    """
    Reads YAML file and return a dictionary
    """
    with open(file_path) as f:
        return yaml.safe_load(f)
