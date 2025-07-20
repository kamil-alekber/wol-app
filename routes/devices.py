"""API routes for device management."""

from flask import Blueprint, request, jsonify, redirect, url_for, flash, Response
from datetime import datetime
from typing import Union, Tuple, TYPE_CHECKING
from models import Device
from utils import generate_device_id

if TYPE_CHECKING:
    from services import DeviceService

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

# Service will be injected by the app factory
device_service: 'DeviceService' = None  # type: ignore


@devices_bp.route('', methods=['GET'])
def get_devices() -> Response:
    """API endpoint to get all devices"""
    devices = device_service.load_devices()
    return jsonify(devices)


@devices_bp.route('', methods=['POST'])
def add_device() -> Union[Response, Tuple[Response, int]]:
    """API endpoint to add a new device"""
    if request.is_json:
        data = request.get_json()
    else:
        data = {
            'name': request.form.get('name'),
            'mac': request.form.get('mac'),
            'ip': request.form.get('ip', ''),
            'description': request.form.get('description', '')
        }
    
    name = data.get('name')
    mac = data.get('mac')
    if not name or not mac:
        if request.is_json:
            return jsonify({'error': 'Name and MAC address are required'}), 400
        else:
            flash('Name and MAC address are required', 'error')
            return redirect(url_for('main.index'))
    
    new_device: Device = {
        'id': generate_device_id(str(name), str(mac)),
        'name': str(name),
        'mac': str(mac).upper(),
        'ip': str(data.get('ip', '')),
        'description': str(data.get('description', '')),
        'created_at': datetime.now().isoformat(),
        'last_wake': None
    }
    
    device_service.add_device(new_device)
    
    if request.is_json:
        return jsonify(new_device), 201
    else:
        flash(f'Device "{new_device["name"]}" added successfully!', 'success')
        return redirect(url_for('main.index'))


@devices_bp.route('/<device_id>', methods=['DELETE'])
def delete_device(device_id: str) -> Union[Response, Tuple[Response, int]]:
    """Delete a device by ID"""
    device = device_service.get_device_by_id(device_id)
    
    if not device:
        if request.is_json:
            return jsonify({'error': 'Device not found'}), 404
        else:
            flash('Device not found', 'error')
            return redirect(url_for('main.index'))

    success = device_service.delete_device(device_id)
    
    if success:
        if request.is_json:
            return jsonify({'message': f'Device "{device["name"]}" deleted successfully'})
        else:
            flash(f'Device "{device["name"]}" deleted successfully!', 'success')
            return redirect(url_for('main.index'))
    else:
        if request.is_json:
            return jsonify({'error': 'Failed to delete device'}), 500
        else:
            flash('Failed to delete device', 'error')
            return redirect(url_for('main.index'))


@devices_bp.route('/<device_id>', methods=['PUT', 'POST'])
def update_device(device_id: str) -> Union[Response, Tuple[Response, int]]:
    """Update a device by ID"""
    device = device_service.get_device_by_id(device_id)
    
    if not device:
        if request.is_json:
            return jsonify({'error': 'Device not found'}), 404
        else:
            flash('Device not found', 'error')
            return redirect(url_for('main.index'))
    
    # Get update data from request
    if request.is_json:
        data = request.get_json()
    else:
        data = {
            'name': request.form.get('name'),
            'mac': request.form.get('mac'),
            'ip': request.form.get('ip', ''),
            'description': request.form.get('description', '')
        }
    
    # Validate required fields
    name = data.get('name')
    mac = data.get('mac')
    if not name or not mac:
        if request.is_json:
            return jsonify({'error': 'Name and MAC address are required'}), 400
        else:
            flash('Name and MAC address are required', 'error')
            return redirect(url_for('main.index'))
    
    # Prepare updates
    updates = {
        'name': str(name),
        'mac': str(mac).upper(),
        'ip': str(data.get('ip', '')),
        'description': str(data.get('description', ''))
    }
    
    success = device_service.update_device(device_id, updates)
    
    if success:
        if request.is_json:
            updated_device = device_service.get_device_by_id(device_id)
            return jsonify(updated_device)
        else:
            flash(f'Device "{updates["name"]}" updated successfully!', 'success')
            return redirect(url_for('main.index'))
    else:
        if request.is_json:
            return jsonify({'error': 'Failed to update device'}), 500
        else:
            flash('Failed to update device', 'error')
            return redirect(url_for('main.index'))


def init_device_routes(ds: 'DeviceService') -> None:
    """Initialize device routes with service dependencies."""
    global device_service
    device_service = ds
