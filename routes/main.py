"""Main routes for device management."""

from flask import Blueprint, render_template
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import DeviceService, MonitoringService

main_bp = Blueprint('main', __name__)

# Services will be injected by the app factory
device_service: 'DeviceService' = None  # type: ignore
monitoring_service: 'MonitoringService' = None  # type: ignore


@main_bp.route('/')
def index() -> str:
    """Main page showing all devices"""
    devices = device_service.load_devices()
    # Add status to each device
    devices_with_status = []
    for device in devices:
        device_id = str(device['id'])  # Convert to string for consistency
        status = monitoring_service.get_device_status(device_id)
        device_with_status = {**device, 'status': status.value}
        devices_with_status.append(device_with_status)
    return render_template('index.html', devices=devices_with_status)


def init_main_routes(ds: 'DeviceService', ms: 'MonitoringService') -> None:
    """Initialize main routes with service dependencies."""
    global device_service, monitoring_service
    device_service = ds
    monitoring_service = ms
