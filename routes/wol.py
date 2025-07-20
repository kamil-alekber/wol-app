"""Wake-on-LAN routes."""

from flask import Blueprint, request, jsonify, redirect, url_for, flash, Response
from typing import Union, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from services import WakeOnLanService

wol_bp = Blueprint('wol', __name__)

# Service will be injected by the app factory
wol_service: 'WakeOnLanService' = None  # type: ignore


@wol_bp.route('/wake/<device_id>', methods=['POST'])
def wake_device(device_id: str) -> Union[Response, Tuple[Response, int]]:
    """Wake up a device by ID"""
    success, message, device = wol_service.wake_device(device_id)
    
    if success:
        if request.is_json:
            return jsonify({'message': message, 'device': device})
        else:
            flash(message, 'success')
            return redirect(url_for('main.index'))
    else:
        status_code = 404 if 'not found' in message.lower() else 500
        if request.is_json:
            return jsonify({'error': message}), status_code
        else:
            flash(message, 'error')
            return redirect(url_for('main.index'))


# Route for form-based deletion (since HTML forms don't support DELETE)
@wol_bp.route('/delete/<device_id>', methods=['POST'])  
def delete_device_form(device_id: str) -> Response:
    """Delete a device by ID via form submission"""
    from routes.devices import device_service
    
    device = device_service.get_device_by_id(device_id)
    
    if not device:
        flash('Device not found', 'error')
        return redirect(url_for('main.index'))

    success = device_service.delete_device(device_id)
    
    if success:
        flash(f'Device "{device["name"]}" deleted successfully!', 'success')
    else:
        flash('Failed to delete device', 'error')
    
    return redirect(url_for('main.index'))


# Route for form-based updates (since HTML forms don't support PUT)
@wol_bp.route('/update/<device_id>', methods=['POST'])  
def update_device_form(device_id: str) -> Response:
    """Update a device by ID via form submission"""
    from routes.devices import device_service
    
    device = device_service.get_device_by_id(device_id)
    
    if not device:
        flash('Device not found', 'error')
        return redirect(url_for('main.index'))
    
    # Get form data
    name = request.form.get('name')
    mac = request.form.get('mac')
    ip = request.form.get('ip', '')
    description = request.form.get('description', '')
    
    # Validate required fields
    if not name or not mac:
        flash('Name and MAC address are required', 'error')
        return redirect(url_for('main.index'))
    
    # Prepare updates
    updates = {
        'name': str(name),
        'mac': str(mac).upper(),
        'ip': str(ip),
        'description': str(description)
    }
    
    success = device_service.update_device(device_id, updates)
    
    if success:
        flash(f'Device "{updates["name"]}" updated successfully!', 'success')
    else:
        flash('Failed to update device', 'error')
    
    return redirect(url_for('main.index'))


def init_wol_routes(ws: 'WakeOnLanService') -> None:
    """Initialize WoL routes with service dependencies."""
    global wol_service
    wol_service = ws
