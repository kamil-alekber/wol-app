"""Discovery routes for network device discovery."""

from flask import Blueprint, jsonify, Response
from datetime import datetime
from typing import Union, Tuple, TYPE_CHECKING
from core.models import Device
from core.utils import generate_device_id

if TYPE_CHECKING:
    from services import DiscoveryService, DeviceService

discovery_bp = Blueprint('discovery', __name__, url_prefix='/discover')

# Services will be injected by the app factory
discovery_service: 'DiscoveryService' = None  # type: ignore
device_service: 'DeviceService' = None  # type: ignore


@discovery_bp.route('/start', methods=['POST'])
def start_discovery() -> Union[Response, Tuple[Response, int]]:
    """Start network device discovery"""
    success = discovery_service.start_discovery()
    
    if not success:
        return jsonify({'error': 'Discovery already in progress'}), 400
    
    return jsonify({'message': 'Discovery started', 'status': 'started'})


@discovery_bp.route('/status', methods=['GET'])
def discovery_status() -> Response:
    """Get current discovery status and results"""
    status = discovery_service.get_discovery_status()
    
    # Load existing devices to check for duplicates
    existing_devices = device_service.load_devices()
    existing_macs = {device['mac'].lower() for device in existing_devices}
    
    # Mark discovered devices as imported if they already exist
    devices_with_status = []
    for device in status['devices']:
        device_copy = device.copy()
        device_copy['already_imported'] = device['mac'].lower() in existing_macs
        devices_with_status.append(device_copy)
    
    status['devices'] = devices_with_status
    return jsonify(status)


@discovery_bp.route('/stop', methods=['POST'])
def stop_discovery() -> Response:
    """Stop network device discovery"""
    discovery_service.stop_discovery()
    return jsonify({'message': 'Discovery stopped', 'status': 'stopped'})


@discovery_bp.route('/import', methods=['POST'])
def import_discovered_devices() -> Response:
    """Import all discovered devices"""
    status = discovery_service.get_discovery_status()
    devices = device_service.load_devices()
    existing_macs = {device['mac'].upper() for device in devices}
    
    imported_count = 0
    for discovered in status['devices']:
        # Skip if MAC already exists
        if discovered['mac'].upper() in existing_macs:
            continue
        
        # Create device name from IP
        id = generate_device_id(discovered['ip'], discovered['mac'])
        device_name = f"Device-{id}"
        
        new_device: Device = {
            'id': id,
            'name': device_name,
            'mac': discovered['mac'],
            'ip': discovered['ip'],
            'description': f"Auto-discovered device",
            'created_at': datetime.now().isoformat(),
            'last_wake': None
        }
        
        device_service.add_device(new_device)
        existing_macs.add(discovered['mac'].upper())
        imported_count += 1
    
    return jsonify({
        'message': f'Imported {imported_count} devices',
        'imported_count': imported_count
    })


@discovery_bp.route('/import/<device_mac>', methods=['POST'])
def import_single_device(device_mac: str) -> Union[Response, Tuple[Response, int]]:
    """Import a single discovered device by MAC address"""
    status = discovery_service.get_discovery_status()
    
    # Find the device in discovery results
    discovered_device = next((d for d in status['devices'] if d['mac'].upper() == device_mac.upper()), None)
    
    if not discovered_device:
        return jsonify({'error': 'Device not found in discovery results'}), 404
    
    devices = device_service.load_devices()
    existing_macs = {device['mac'].upper() for device in devices}
    
    # Check if device already exists
    if discovered_device['mac'].upper() in existing_macs:
        return jsonify({'error': 'Device already exists'}), 400
    
    id = generate_device_id(discovered_device['ip'], discovered_device['mac'])
    device_name = f"Device-{id}"
    
    new_device: Device = {
        'id': id,
        'name': device_name,
        'mac': discovered_device['mac'],
        'ip': discovered_device['ip'],
        'description': f"Auto-discovered device",
        'created_at': datetime.now().isoformat(),
        'last_wake': None
    }
    
    device_service.add_device(new_device)
    
    return jsonify({
        'message': f'Device "{device_name}" imported successfully',
        'device': new_device
    })


def init_discovery_routes(ds: 'DiscoveryService', device_svc: 'DeviceService') -> None:
    """Initialize discovery routes with service dependencies."""
    global discovery_service, device_service
    discovery_service = ds
    device_service = device_svc
