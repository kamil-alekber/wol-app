"""Service for monitoring device status."""

import threading
import time
from typing import Dict
from models import DeviceStatus
from services.device_service import DeviceService
from utils import ping_device
from config import config


class MonitoringService:
    """Service class for monitoring device status."""
    
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service
        self.device_status: Dict[str, DeviceStatus] = {}
        self._monitoring_thread: threading.Thread | None = None
        self._stop_monitoring = False
    
    def start_monitoring(self) -> None:
        """Start the device monitoring thread."""
        if self._monitoring_thread is None or not self._monitoring_thread.is_alive():
            self._stop_monitoring = False
            self._monitoring_thread = threading.Thread(target=self._monitor_devices, daemon=True)
            self._monitoring_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop the device monitoring thread."""
        self._stop_monitoring = True
    
    def get_device_status(self, device_id: str) -> DeviceStatus:
        """Get the status of a specific device."""
        return self.device_status.get(device_id, DeviceStatus.UNKNOWN)
    
    def get_all_statuses(self) -> Dict[str, str]:
        """Get all device statuses as a dictionary."""
        return {device_id: status.value for device_id, status in self.device_status.items()}
    
    def _monitor_devices(self) -> None:
        """Background thread to monitor device status."""
        while not self._stop_monitoring:
            devices = self.device_service.load_devices()
            for device in devices:
                device_id = str(device['id'])  # Convert to string for consistency
                if device.get('ip'):  # Only ping devices with IP addresses
                    status = ping_device(device['ip'])
                    self.device_status[device_id] = DeviceStatus.ONLINE if status else DeviceStatus.OFFLINE
                else:
                    self.device_status[device_id] = DeviceStatus.UNKNOWN
            time.sleep(config.monitoring_interval)
