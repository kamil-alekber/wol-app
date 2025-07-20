"""Status and monitoring routes."""

from flask import Blueprint, jsonify, Response
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services import MonitoringService

status_bp = Blueprint('status', __name__)

# Service will be injected by the app factory  
monitoring_service: 'MonitoringService' = None  # type: ignore


@status_bp.route('/status')
def get_status() -> Response:
    """API endpoint to get device status"""
    status_dict = monitoring_service.get_all_statuses()
    return jsonify(status_dict)


def init_status_routes(ms: 'MonitoringService') -> None:
    """Initialize status routes with service dependencies."""
    global monitoring_service
    monitoring_service = ms
