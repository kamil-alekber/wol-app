"""Main application factory for the Wake-on-LAN Flask application."""

from flask import Flask
from config import config
from services import DeviceService, MonitoringService, DiscoveryService, WakeOnLanService
from routes import (
    main_bp, devices_bp, status_bp, wol_bp, discovery_bp,
    init_main_routes, init_device_routes, init_status_routes, 
    init_wol_routes, init_discovery_routes
)


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = config.app_secret_key
    
    # Initialize services
    device_service = DeviceService()
    monitoring_service = MonitoringService(device_service)
    discovery_service = DiscoveryService()
    wol_service = WakeOnLanService(device_service)
    
    # Initialize route dependencies
    init_main_routes(device_service, monitoring_service)
    init_device_routes(device_service)
    init_status_routes(monitoring_service)
    init_wol_routes(wol_service)
    init_discovery_routes(discovery_service, device_service)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(wol_bp)
    app.register_blueprint(discovery_bp)
    
    # Start monitoring service
    monitoring_service.start_monitoring()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.app_debug, host=config.app_host, port=config.app_port)
