from typing import List, Tuple

import pytest

from pydantic import BaseModel, errors
from pychu.args import args


class SimpleModel(BaseModel):
    option_a: str
    option_b: int


def test_simple_model():
    provider = args(argv=["--option-a", "test", "--option-b", "123"])
    config = provider(SimpleModel)

    assert config["option_a"] == "test"
    assert config["option_b"] == 123
    assert len(config) == 2, "Ensuring no extra field is present"

    with pytest.raises(errors.ExtraError):
        provider = args(argv=["--option-a", "test", "--option-b", "123", "--unknown-option", "nope"])
        provider(SimpleModel)


class NestedModel(BaseModel):
    nested: SimpleModel
    option_c: int


def test_nested_model():
    provider = args(argv=["--nested-option-a", "test", "--nested-option-b", "123", "--option-c", "456"])
    config = provider(NestedModel)

    assert config["nested"]["option_a"] == "test"
    assert config["nested"]["option_b"] == 123
    assert config["option_c"] == 456
    assert len(config) == 2 and len(config["nested"]) == 2, "Ensuring no extra field is present"


class ModelWithTuple(BaseModel):
    coordinates: Tuple[int, int]


def test_model_with_tuple():
    provider = args(argv=["--coordinates", "1", "2"])
    config = provider(ModelWithTuple)

    assert config["coordinates"][0] == 1
    assert config["coordinates"][1] == 2
    assert len(config) == 1 and len(config["coordinates"]) == 2, "Ensuring no extra field is present"


class ModelWithList(BaseModel):
    values: List[int]


def test_model_with_list():
    provider = args(argv=["--values", "1", "--values", "2", "--values", "3"])
    config = provider(ModelWithList)

    assert config["values"][0] == 1
    assert config["values"][1] == 2
    assert config["values"][2] == 3
    assert len(config) == 1 and len(config["values"]) == 3, "Ensuring no extra field is present"


class ModelWithBool(BaseModel):
    a_flag: bool


def test_model_with_bool():
    provider = args(argv=["--a-flag"])
    config = provider(ModelWithBool)

    assert config["a_flag"] is True
