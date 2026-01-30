"""
Example Celery tasks for testing and demonstration.
"""

import time
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def add(self, x: int, y: int) -> int:
    """
    Simple addition task.

    Args:
        x: First number
        y: Second number

    Returns:
        Sum of x and y
    """
    try:
        logger.info(f"Adding {x} + {y}")
        result = x + y
        logger.info(f"Result: {result}")
        return result
    except Exception as exc:
        logger.error(f"Error in add task: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def long_running_task(self, duration: int = 10) -> dict:
    """
    Simulates a long-running task (e.g., deployment, build).

    Args:
        duration: Duration in seconds

    Returns:
        Task completion info
    """
    try:
        logger.info(f"Starting long-running task for {duration} seconds")

        for i in range(duration):
            logger.info(f"Progress: {i + 1}/{duration}")
            time.sleep(1)

        logger.info("Long-running task completed")
        return {
            "status": "completed",
            "duration": duration,
            "message": f"Task ran for {duration} seconds",
        }
    except Exception as exc:
        logger.error(f"Error in long_running_task: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_deployment(self, deployment_id: str, service_name: str) -> dict:
    """
    Example deployment task.

    Args:
        deployment_id: Unique deployment identifier
        service_name: Name of the service to deploy

    Returns:
        Deployment result
    """
    try:
        logger.info(f"Processing deployment {deployment_id} for service {service_name}")

        # Simulate deployment steps
        steps = [
            "Pulling code from repository",
            "Installing dependencies",
            "Building application",
            "Running tests",
            "Deploying to production",
            "Health checks",
        ]

        for step in steps:
            logger.info(f"[{deployment_id}] {step}")
            time.sleep(1)

        logger.info(f"Deployment {deployment_id} completed successfully")
        return {
            "deployment_id": deployment_id,
            "service_name": service_name,
            "status": "success",
            "message": "Deployment completed successfully",
        }
    except Exception as exc:
        logger.error(f"Error in process_deployment: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def monitor_service(self, service_id: str) -> dict:
    """
    Example monitoring task.

    Args:
        service_id: Service identifier to monitor

    Returns:
        Service health status
    """
    try:
        logger.info(f"Monitoring service {service_id}")

        # Simulate health check
        health_status = {
            "service_id": service_id,
            "cpu_usage": 45.2,
            "memory_usage": 62.8,
            "uptime": 3600,
            "status": "healthy",
        }

        logger.info(f"Service {service_id} health: {health_status}")
        return health_status
    except Exception as exc:
        logger.error(f"Error in monitor_service: {exc}")
        raise self.retry(exc=exc, countdown=60)
