"""Utility functions for the WoL application."""

import hashlib
import subprocess
from config import config


def generate_device_id(name: str, mac: str) -> str:
    """Generate a short hash-based ID for a device using name and MAC address"""
    # Combine name and MAC for unique input
    combined = f"{name}_{mac}".encode('utf-8')
    # Generate hash and take first 8 characters for a short ID
    hash_obj = hashlib.sha256(combined)
    device_id = hash_obj.hexdigest()[:8]
    
    return device_id


def ping_device(ip_address: str) -> bool:
    """Ping a device and return True if all packets are successful"""
    cmd = [config.ping_command, '-c', str(config.ping_count), ip_address]
    try:
        result = subprocess.run(cmd, 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print(f"Ping command not found: {config.ping_command}")
        return False
    except Exception:
        return False
