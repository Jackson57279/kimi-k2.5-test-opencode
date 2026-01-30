"""
Celery application configuration with Redis broker and result backend.
"""

import os
import sys
from celery import Celery
from kombu import Exchange, Queue

# Add backend to path for task discovery
sys.path.insert(0, os.path.dirname(__file__))

# Initialize Celery app
app = Celery("railway_paas")

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery configuration
app.conf.update(
    # Broker and result backend
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Task execution settings
    task_track_started=True,
    task_time_limit=3600,  # 1 hour hard limit
    task_soft_time_limit=3300,  # 55 minutes soft limit
    # Worker settings
    worker_prefetch_multiplier=1,  # Fair distribution - process one task at a time
    worker_max_tasks_per_child=1000,
    # Task retry settings
    task_autoretry_for=(Exception,),
    task_max_retries=3,
    task_default_retry_delay=60,  # Retry after 60 seconds
    # Queue configuration
    task_queues=(
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("build", Exchange("build"), routing_key="build"),
        Queue("deploy", Exchange("deploy"), routing_key="deploy"),
        Queue("monitor", Exchange("monitor"), routing_key="monitor"),
    ),
    # Default queue
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    # Task routing
    task_routes={
        "backend.tasks.build.*": {"queue": "build"},
        "backend.tasks.deploy.*": {"queue": "deploy"},
        "backend.tasks.monitor.*": {"queue": "monitor"},
    },
)

# Import tasks directly
from tasks import add, long_running_task, process_deployment, monitor_service


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f"Request: {self.request!r}")
