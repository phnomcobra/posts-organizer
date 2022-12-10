"""This module implements the validation classes for configuring the post organizer."""
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import BaseModel
import toml

class Server(BaseModel):
    host: IPv4Address | None = IPv4Address("0.0.0.0")
    port: int | None = 8080

class Paths(BaseModel):
    boxes: Path | None = Path("./boxes")
    logging: Path | None = Path("./log")

class Configuration(BaseModel):
    paths: Paths
    server: Server

CONFIG = Configuration(**toml.load('config.toml'))
