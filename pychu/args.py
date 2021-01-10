"""
Provider suitable to load configuration from program arguments
"""

import argparse
import sys
from typing import Any, Dict, List, Type

from pydantic.errors import ExtraError

from ._dict_utils import get_paths, insert_at_path
from ._types import Provider, Model

_TYPENAME_TO_TYPE = {
    "integer": int,
    "string": str,
    "number": float,
}


class _StoreTrueOrNone(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)


def _make_tuple_action(types):
    class TupleAction(argparse.Action):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tuple_types = types

        def __call__(self, parser, namespace, values, option_string=None):
            assert len(values) == len(self.tuple_types)
            values = tuple(_TYPENAME_TO_TYPE[t](v) for v, t in zip(values, self.tuple_types))
            setattr(namespace, self.dest, values)

    return TupleAction


def _path_to_flag_name(path) -> str:
    name = '-'.join(path).replace('_', '-')
    return name


def _flag_name_to_path(flag_name: str):
    flag_name = flag_name.lstrip('--')
    return tuple(flag_name.split('-'))


def _is_basic_type(type_: str) -> bool:
    return type_ in {"string", "integer", "number"}


def _is_supported_type(type_: str) -> bool:
    return type_ in {"string", "integer", "number", "boolean", "array"}


def _add_argument_for(parser: argparse.ArgumentParser, name, type_, schema):
    if type_ == "boolean":
        parser.add_argument(f"--{name}", action=_StoreTrueOrNone, nargs=0, required=False)
    elif _is_basic_type(type_):
        parser.add_argument(f"--{name}", type=_TYPENAME_TO_TYPE[type_], metavar="[value]", required=False)
    elif type_ == "array":
        items = schema["items"]
        if isinstance(items, dict):
            value_type = items["type"]
            if _is_basic_type(value_type):
                parser.add_argument(
                    f"--{name}",
                    action='append',
                    type=_TYPENAME_TO_TYPE[value_type],
                    metavar="[value]",
                    required=False,
                )
        else:
            assert isinstance(items, list)
            items_types = [i["type"] for i in items]
            if all(_is_basic_type(t) for t in items_types):
                parser.add_argument(
                    f"--{name}",
                    nargs=len(items_types),
                    action=_make_tuple_action(items_types),
                    metavar="[value]",
                    required=False,
                )


def _argument_parser_for(target: Type[Model]):
    arg_to_path = {}
    parser = argparse.ArgumentParser(allow_abbrev=False, add_help=True)
    paths = ((path, type_, sch) for path, type_, sch in get_paths(target) if _is_supported_type(type_))

    for path, type_, sch in paths:
        arg_name = _path_to_flag_name(path)
        arg_to_path[arg_name] = path
        _add_argument_for(parser, arg_name, type_, sch)
    return parser, arg_to_path


def argument_parser_for(target: Type[Model]) -> argparse.ArgumentParser:
    """
    Retrieve an argument parser suitable for a given type

    :param target:                  the target type
    """

    return _argument_parser_for(target)[0]


def args(
        argv: List[str] = None,
) -> Provider:
    """
    Configure a provider that reads from the program arguments

    :param argv:                    the argument vector to parse from
    """

    argv = argv if argv is not None else sys.argv[1:]

    def load_from_args(target: Type[Model]) -> Dict[str, Any]:
        parser, arg_to_path = _argument_parser_for(target)
        parsed, unknown = parser.parse_known_args(argv)
        if unknown:
            raise ExtraError
        result = {}
        for name, value in vars(parsed).items():
            if value is not None:
                insert_at_path(result, arg_to_path[name.replace("_", "-")], value)
        return result

    return load_from_args
