from typing import Dict, Any
import os
import yaml


def set_env_variables_from_yaml(file_path: str) -> Dict[str, Any]:
    """Load environment variables from a YAML file."""
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    return config


if __name__ == "__main__":
    config = set_env_variables_from_yaml("config.yaml")

    print(config)
