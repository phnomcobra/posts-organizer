"""This module implements the argument parser and validation classes for
configuring the post organizer."""
import argparse
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import BaseModel, PositiveInt
import toml

class Server(BaseModel): # pylint: disable=too-few-public-methods
    """This class encapsulates and validates the server settings."""
    host: IPv4Address | None = IPv4Address("0.0.0.0")
    port: PositiveInt | None = 8080
    retention_seconds: PositiveInt | None = 3600

class Paths(BaseModel): #  pylint: disable=too-few-public-methods
    """The class encapsulates and validates the path settings."""
    boxes: Path | None = Path("./boxes")
    logging: Path | None = Path("./log")

class Logging(BaseModel): #  pylint: disable=too-few-public-methods
    """The class encapsulates and validates the logging settings."""
    retention_days: PositiveInt | None = 30

class Configuration(BaseModel): # pylint: disable=too-few-public-methods
    """This class is the root level of encapsulation for the configuration settings."""
    paths: Paths
    server: Server
    logging: Logging

parser = argparse.ArgumentParser(description = 'Posts Organizer')
parser.add_argument('-f', dest='config_file', action='store', default='config.toml')
kwargs = vars(parser.parse_args())
CONFIG = Configuration(**toml.load(kwargs['config_file']))
