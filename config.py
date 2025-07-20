import json
import os
from typing import Dict, Any

class Config:
    """Configuration manager for the WOL app"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            print(f"Warning: Configuration file '{self.config_file}' not found.")
            print("Please copy config.example.json to config.json and customize it.")
            print("Using default configuration for now...")
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            print("Using default configuration...")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration when config file is missing or invalid"""
        return {
            "app": {
                "secret_key": "default-secret-key-change-me",
                "debug": True,
                "host": "127.0.0.1",
                "port": 5000
            },
            "monitoring": {
                "interval_seconds": 30,
                "ping_count": 4
            },
            "paths": {
                "devices_file": "devices.json",
                "ping_command": "/usr/bin/ping",
                "arping_command": "/usr/bin/arping",
                "wakeonlan_command": "/usr/bin/wakeonlan"
            },
            "network": {
                "local_network": "192.168.1.0/24"
            }
        }
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value by section and key"""
        return self._config.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get an entire configuration section"""
        return self._config.get(section, {})
    
    @property
    def app_secret_key(self) -> str:
        return self.get('app', 'secret_key', 'default-secret-key')
    
    @property
    def app_debug(self) -> bool:
        return self.get('app', 'debug', False)
    
    @property
    def app_host(self) -> str:
        return self.get('app', 'host', '127.0.0.1')
    
    @property
    def app_port(self) -> int:
        return self.get('app', 'port', 5000)
    
    @property
    def monitoring_interval(self) -> int:
        return self.get('monitoring', 'interval_seconds', 30)
    
    @property
    def ping_count(self) -> int:
        return self.get('monitoring', 'ping_count', 4)
    
    @property
    def devices_file(self) -> str:
        return self.get('paths', 'devices_file', 'devices.json')
    
    @property
    def ping_command(self) -> str:
        return self.get('paths', 'ping_command', '/usr/bin/ping')
    
    @property
    def arping_command(self) -> str:
        return self.get('paths', 'arping_command', '/usr/bin/arping')
    
    @property
    def wakeonlan_command(self) -> str:
        return self.get('paths', 'wakeonlan_command', '/usr/bin/wakeonlan')
    
    @property
    def local_network(self) -> str:
        return self.get('network', 'local_network', '192.168.1.0/24')

# Global configuration instance
config = Config()
