"""
Provider suitable to load configuration from TOML files
"""

from typing import Any, Dict

import toml as _toml


def toml(file: str, must_exist: bool = True):
    """
    Configure a provider that reads from a TOML file

    :param file:                        the path to the TOML file
    :param must_exist:                  whether or not the file must exist
    """

    def load_from_toml_file(_) -> Dict[str, Any]:
        result = {}
        try:
            with open(file) as toml_file:
                result = _toml.load(toml_file)
        except FileNotFoundError:
            if must_exist is True:
                raise
        return result

    return load_from_toml_file
