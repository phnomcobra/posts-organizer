"""This module implements the validation classes for configuring the post organizer."""
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import BaseModel
import toml

class Server(BaseModel): # pylint: disable=too-few-public-methods
    """This class encapsulates and validates the web server settings."""
    host: IPv4Address | None = IPv4Address("0.0.0.0")
    port: int | None = 8080

class Paths(BaseModel): #  pylint: disable=too-few-public-methods
    """The class encapsulates and validates the path settings."""
    boxes: Path | None = Path("./boxes")
    logging: Path | None = Path("./log")

class Configuration(BaseModel): # pylint: disable=too-few-public-methods
    """This class is the root level of encapsulation for the configuration settings."""
    paths: Paths
    server: Server

CONFIG = Configuration(**toml.load('config.toml'))
