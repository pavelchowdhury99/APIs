import yaml
import logging


def read_yaml(file_path):
    """
    Reads YAML file and return a dictionary
    """
    with open(file_path) as f:
        return yaml.safe_load(f)


def get_logger():
    """
    Return a logger object
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
