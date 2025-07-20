"""Data models and type definitions for the WoL application."""

from enum import Enum
from typing import Optional, TypedDict


class Device(TypedDict):
    id: str
    name: str
    mac: str
    ip: str
    description: str
    created_at: str
    last_wake: Optional[str]


class DeviceWithStatus(Device):
    status: str


class DiscoveredDevice(TypedDict):
    mac: str
    ip: str


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"
