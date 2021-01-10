#!/usr/bin/env python3

from pydantic import BaseModel
from pychu.args import args
from pychu.env import env
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
        env(prefix="RABBITMQ_"),
        json("./config.json")
    ]
)
print(rabbitmq)
