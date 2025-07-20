"""Service for managing device data persistence."""

import json
import os
from typing import List, Dict, Any
from models import Device
from config import config


class DeviceService:
    """Service class for handling device CRUD operations."""
    
    def __init__(self):
        self.devices_file = config.devices_file
    
    def load_devices(self) -> List[Device]:
        """Load devices from JSON file"""
        if os.path.exists(self.devices_file):
            try:
                with open(self.devices_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_devices(self, devices: List[Device]) -> None:
        """Save devices to JSON file"""
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=2)
    
    def get_device_by_id(self, device_id: str) -> Device | None:
        """Get a device by its ID"""
        devices = self.load_devices()
        return next((d for d in devices if str(d['id']) == device_id), None)
    
    def add_device(self, device: Device) -> None:
        """Add a new device"""
        devices = self.load_devices()
        devices.append(device)
        self.save_devices(devices)
    
    def delete_device(self, device_id: str) -> bool:
        """Delete a device by ID. Returns True if device was found and deleted."""
        devices = self.load_devices()
        original_length = len(devices)
        devices = [d for d in devices if d['id'] != device_id]
        
        if len(devices) < original_length:
            self.save_devices(devices)
            return True
        return False
    
    def update_device(self, device_id: str, updates: Dict[str, Any]) -> bool:
        """Update a device. Returns True if device was found and updated."""
        devices = self.load_devices()
        
        for device in devices:
            if str(device['id']) == device_id:
                for key, value in updates.items():
                    if key in device:
                        device[key] = value  # type: ignore
                self.save_devices(devices)
                return True
        return False
