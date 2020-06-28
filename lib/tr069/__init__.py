"""
A TR-069 Honeyclient implementation.
"""
from .client import Client
from .connection_request_server import ConnectionRequestServer
from .data import device
from .data import event
from .data import parameters
from .data import rpcs

__version__ = '1.0'
__all__ = [
    "Client",
    "ConnectionRequestServer",
    "device",
    "event",
    "parameters",
    "rpcs",
]
