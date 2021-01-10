"""
Internal helpers to deal with nested dicts
"""

from typing import Any, Dict, List, Tuple, Type, TypeVar

from ._types import Model

Path = Tuple[str, ...]


def _resolve_refs_dict(definitions: Dict[str, Any], schema: Dict[str, Any]):
    ref = schema.get("$ref")
    if ref is not None:
        schema = definitions[ref]
    for key, value in schema.items():
        schema[key] = _resolve_refs(definitions, value)
    return schema


_JsonObject = TypeVar("_JsonObject", Dict[str, Any], List[Any], str, float, int)


def _resolve_refs(definitions, v: _JsonObject) -> _JsonObject:
    if isinstance(v, dict):
        return _resolve_refs_dict(definitions, v)
    if isinstance(v, list):
        return [_resolve_refs(definitions, e) for e in v]
    return v


def _get_paths(schema: Dict[str, Any], path: Path = ()):
    type_ = schema["type"]
    if type_ == "object" and "properties" in schema:
        for prop, subschema in schema["properties"].items():
            yield from _get_paths(subschema, (*path, prop))
    else:
        yield path, type_, schema


def get_paths(model: Type[Model]):
    """
    Generate all the paths for a given model
    """

    schema = model.schema(ref_template="{model}").copy()
    defs = schema.pop("definitions", None)
    if defs is not None:
        schema = _resolve_refs(defs, schema)
    return _get_paths(schema)


def insert_at_path(nested: Dict[str, Any], path: Path, value: Any):
    """
    Insert a value at a given path in a nested dict
    """

    *firsts, last = path
    for comp in firsts:
        if comp not in nested:
            nested[comp] = {}
        nested = nested[comp]
    nested[last] = value
