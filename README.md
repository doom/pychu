# pychu

[![pytest](https://github.com/doom/pychu/workflows/pytest/badge.svg)](https://github.com/doom/pychu/actions?query=branch%3Amain)
[![pypi](https://img.shields.io/pypi/v/pychu.svg)](https://pypi.python.org/pypi/pychu)
[![license](https://img.shields.io/github/license/doom/pychu.svg)](https://github.com/doom/pychu/blob/main/LICENSE)

Layered configuration loading built on [Pydantic](https://pydantic-docs.helpmanual.io/).

With Pychu, you can define your program's configuration as a Pydantic model, then load it from multiple providers.
Providers are ordered as levels of layers, thus allowing upper layers to override values from lower layers.

At the moment, the following providers are implemented :
- Program arguments
- Environment variables
- JSON
- TOML (with the `pychu[toml]` extension)
- YAML (with the `pychu[yaml]` extension)

## Requirements

Pychu requires Python 3.6+ and Pydantic 1.7.3+.

## Installing

Pychu can be installed through pip.

```
$ pip3 install pychu        # Install the basic version
$ pip3 install pychu[yaml]  # Install the YAML extension
```

## Example

The following example loads configuration from a JSON file, but also allows overriding using program arguments.

```python
from pydantic import BaseModel
from pychu.args import args
from pychu.json import json
from pychu import load

class RabbitMQ(BaseModel):
    host: str
    username: str
    password: str
    port: int = 5671

rabbitmq = load(
    target=RabbitMQ,
    providers=[
        args(),
        json("./config.json")
    ]
)
print(rabbitmq)
```

```
$ cat config.json
{"host": "localhost", "port": 5671, "username": "user", "password": "pass"}
$ ./example.py
host='localhost' username='user' password='pass' port=5671
$ ./example.py --port 5672
host='localhost' username='user' password='pass' port=5672
```
