from contextlib import contextmanager
import os
from typing import List

from pydantic import BaseModel
from pychu.env import env


@contextmanager
def push_env(**kwargs):
    old_env = os.environ.copy()
    for k, v in kwargs.items():
        os.environ[k] = v
    try:
        yield
    finally:
        os.environ = old_env


class SimpleModel(BaseModel):
    option_a: str
    option_b: int


def test_simple_model():
    with push_env(OPTION_A="test", OPTION_B="123"):
        provider = env()
        config = provider(SimpleModel)

        assert config["option_a"] == "test"
        assert config["option_b"] == "123"
        assert len(config) == 2, "Ensuring no extra field is present"


class NestedModel(BaseModel):
    nested: SimpleModel
    option_c: int


def test_nested_model():
    with push_env(NESTED_OPTION_A="test", NESTED_OPTION_B="123", OPTION_C="456"):
        provider = env()
        config = provider(NestedModel)

        assert config["nested"]["option_a"] == "test"
        assert config["nested"]["option_b"] == "123"
        assert config["option_c"] == "456"
        assert len(config) == 2 and len(config["nested"]) == 2, "Ensuring no extra field is present"


class ModelWithList(BaseModel):
    values: List[int]
    opt: int


def test_model_with_list():
    with push_env(VALUES="1,2,3", OPT="1"):
        provider = env(allow_arrays=True)
        config = provider(ModelWithList)

        assert config["values"][0] == "1"
        assert config["values"][1] == "2"
        assert config["values"][2] == "3"
        assert len(config) == 2 and len(config["values"]) == 3, "Ensuring no extra field is present"


def test_model_with_list_without_allowing():
    with push_env(VALUES="1,2,3", OPT="1"):
        provider = env(allow_arrays=False)
        config = provider(ModelWithList)

        assert len(config) == 1  # lists are ignored
        assert config["opt"] == "1"
