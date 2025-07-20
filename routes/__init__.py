"""Route blueprints initialization."""

from .main import main_bp, init_main_routes
from .devices import devices_bp, init_device_routes  
from .status import status_bp, init_status_routes
from .wol import wol_bp, init_wol_routes
from .discovery import discovery_bp, init_discovery_routes

__all__ = [
    'main_bp',
    'devices_bp', 
    'status_bp',
    'wol_bp',
    'discovery_bp',
    'init_main_routes',
    'init_device_routes',
    'init_status_routes', 
    'init_wol_routes',
    'init_discovery_routes'
]
