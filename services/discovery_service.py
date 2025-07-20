"""Service for network discovery functionality."""

import re
import subprocess
import threading
import time
import ipaddress
from typing import List, Optional, Dict, Any
from models import DiscoveredDevice
from config import config


class DiscoveryService:
    """Service class for network device discovery."""
    
    def __init__(self):
        self.discovery_active: bool = False
        self.discovery_results: List[DiscoveredDevice] = []
        self.discovery_thread: Optional[threading.Thread] = None
    
    def start_discovery(self) -> bool:
        """Start network device discovery. Returns True if started successfully."""
        if self.discovery_active:
            return False
        
        # Start discovery in background thread
        self.discovery_thread = threading.Thread(target=self._network_discovery_worker, daemon=True)
        self.discovery_thread.start()
        return True
    
    def stop_discovery(self) -> None:
        """Stop network device discovery."""
        self.discovery_active = False
    
    def get_discovery_status(self) -> Dict[str, Any]:
        """Get current discovery status and results."""
        return {
            'active': self.discovery_active,
            'count': len(self.discovery_results),
            'devices': self.discovery_results.copy()
        }
    
    def clear_results(self) -> None:
        """Clear discovery results."""
        self.discovery_results.clear()
    
    def _discover_device_by_ip(self, ip: str) -> Optional[DiscoveredDevice]:
        """Discover a single device by IP address using arping to find MAC address"""
        try:
            arping_result = subprocess.run([config.arping_command, '-c', '1', '-w', '1', ip], 
                                         capture_output=True, text=True, timeout=3)
            
            if arping_result.returncode == 0 and arping_result.stdout:
                mac_match = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', arping_result.stdout)
                if mac_match:
                    mac = mac_match.group(0).upper().replace('-', ':')
                    return {
                        'mac': mac,
                        'ip': ip
                    }
            
            return None
            
        except FileNotFoundError:
            print(f"Error: 'arping' command not found at {config.arping_command}. Please install arping utility or update the arping_command path in config.json.")
            return None
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
            return None
    
    def _network_discovery_worker(self) -> None:
        """Background worker for network discovery"""
        self.discovery_active = True
        self.discovery_results.clear()
        
        try:
            network_obj = ipaddress.IPv4Network(config.local_network, strict=False)
            ips_to_scan = [str(ip) for ip in network_obj.hosts()]
            
            # Use threading to scan multiple IPs concurrently
            def scan_ip(ip: str) -> None:
                device = self._discover_device_by_ip(ip)
                if device:
                    self.discovery_results.append(device)
            
            # Scan in batches to avoid overwhelming the network
            batch_size = 20
            
            for i in range(0, len(ips_to_scan), batch_size):
                batch = ips_to_scan[i:i + batch_size]
                batch_threads: List[threading.Thread] = []

                for ip in batch:
                    if not self.discovery_active: 
                        break
                        
                    thread = threading.Thread(target=scan_ip, args=(ip,))
                    thread.start()
                    batch_threads.append(thread)
                
                for thread in batch_threads:
                    thread.join(timeout=5)  
                
                if not self.discovery_active:
                    break
                    
                time.sleep(0.1)
        
        except Exception as e:
            print(f"Network discovery error: {e}")
        
        finally:
            self.discovery_active = False
