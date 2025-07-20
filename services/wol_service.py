"""Service for Wake-on-LAN functionality."""

import subprocess
from datetime import datetime
from models import Device
from services.device_service import DeviceService
from config import config


class WakeOnLanService:
    """Service class for Wake-on-LAN operations."""
    
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service
    
    def wake_device(self, device_id: str) -> tuple[bool, str, Device | None]:
        """
        Wake up a device by ID.
        Returns (success, message, device).
        """
        device = self.device_service.get_device_by_id(device_id)
        
        if not device:
            return False, 'Device not found', None
        
        try:
            subprocess.run([config.wakeonlan_command, device['mac']], 
                          capture_output=True, text=True, check=True)
            
            # Update last wake time
            updates = {'last_wake': datetime.now().isoformat()}
            self.device_service.update_device(device_id, updates)
            
            # Get updated device
            updated_device = self.device_service.get_device_by_id(device_id)
            
            message = f'Wake-on-LAN packet sent to {device["name"]} ({device["mac"]})'
            return True, message, updated_device
            
        except subprocess.CalledProcessError as e:
            error_msg = f'Failed to wake {device["name"]}: {e}'
            return False, error_msg, device
        except FileNotFoundError:
            error_msg = 'wakeonlan command not found. Please install it first.'
            return False, error_msg, device
