"""
Celery tasks module.
"""

from .example import add, long_running_task, process_deployment, monitor_service

__all__ = [
    "add",
    "long_running_task",
    "process_deployment",
    "monitor_service",
]
