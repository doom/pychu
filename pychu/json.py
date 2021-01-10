"""
Provider suitable to load configuration from JSON files
"""

from typing import Any, Dict

import json as _json


def json(file: str, must_exist: bool = True):
    """
    Configure a provider that reads from a JSON file

    :param file:                        the path to the JSON file
    :param must_exist:                  whether or not the file must exist
    """

    def load_from_json_file(_) -> Dict[str, Any]:
        result = {}
        try:
            with open(file) as json_file:
                result = _json.load(json_file)
        except FileNotFoundError:
            if must_exist is True:
                raise
        return result

    return load_from_json_file
