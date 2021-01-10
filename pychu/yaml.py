"""
Provider suitable to load configuration from YAML files
"""

from typing import Any, Dict

import yaml as _yaml


def yaml(file: str, must_exist: bool = True):
    """
    Configure a provider that reads from a YAML file

    :param file:                        the path to the YAML file
    :param must_exist:                  whether or not the file must exist
    """

    def load_from_yaml_file(_) -> Dict[str, Any]:
        result = {}
        try:
            with open(file) as yaml_file:
                result = _yaml.safe_load(yaml_file)
        except FileNotFoundError:
            if must_exist is True:
                raise
        return result

    return load_from_yaml_file
