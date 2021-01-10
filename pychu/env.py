"""
Provider suitable to load configuration from the program environment
"""

import os
from typing import Any, Dict, Type

from ._dict_utils import get_paths, insert_at_path
from ._types import Provider, Model


def env(
        prefix: str = None,
        allow_arrays: bool = False,
        array_separator: str = ',',
) -> Provider:
    """
    Configure a provider that reads from the program environment

    :param prefix:                      the prefix to use for each environment variable name (or None for no prefix)
    :param allow_arrays:                whether or not lists should be parsed from environment variables
    :param array_separator:             the separator to use to split values when parsing lists
    """

    def load_from_env(target: Type[Model]) -> Dict[str, Any]:
        variable_prefix = prefix or ""
        paths = ((p, t) for p, t, _ in get_paths(target))

        if not allow_arrays:
            paths = ((p, t) for p, t in paths if t != "array")

        result = {}
        for (path, type_) in paths:
            var_name = variable_prefix + "_".join(map(str.upper, path))
            value = os.environ.get(var_name)
            if value is None:
                continue
            if type_ == "array":
                value = value.split(array_separator)
            insert_at_path(result, path, value)

        return result

    return load_from_env
