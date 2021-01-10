from typing import Any, Callable, Dict, Reversible, Type

from ._types import Provider, Model

Merger = Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]
OverrideStrategy = Callable[[Any, Any, Merger], Any]


def _override_by_merging_collections(bottom_value: Any, top_value: Any, merge: Merger):
    """
    Override strategy that merges collections and replaces lower-priority values with higher-priority values
    """
    if isinstance(bottom_value, dict) and isinstance(top_value, dict):
        return merge(bottom_value, top_value)
    if isinstance(bottom_value, list) and isinstance(top_value, list):
        return bottom_value + top_value
    return top_value


def _override_by_replacing(bottom_value: Any, top_value: Any, merge: Merger):
    """
    Override strategy that replaces lower-priority values with higher-priority values
    """
    return top_value


MERGE_COLLECTIONS = _override_by_merging_collections
REPLACE = _override_by_replacing


def _merge_dicts(bottom_dict: Dict[str, Any], top_dict: Dict[str, Any], strategy: OverrideStrategy) -> Dict[str, Any]:
    for key, top_value in top_dict.items():
        bottom_value = bottom_dict.get(key)
        if bottom_value is None:
            bottom_dict[key] = top_value
        else:
            bottom_dict[key] = _override_by_merging_collections(
                bottom_value,
                top_value,
                lambda a, b: _merge_dicts(a, b, strategy)
            )
    return bottom_dict


def load(
        target: Type[Model],
        providers: Reversible[Provider],
        override_strategy: OverrideStrategy = MERGE_COLLECTIONS
) -> Model:
    """
    Load a model instance using the given providers

    :param target:                      the target model type
    :param providers:                   the list of providers to use, in descending order of priority
    :param override_strategy            a strategy defining how a higher-priority layer overrides a lower-priority layer
    """

    result = {}
    for provider in reversed(providers):
        data = provider(target)
        result = _merge_dicts(result, data, override_strategy)
    return target(**result)
